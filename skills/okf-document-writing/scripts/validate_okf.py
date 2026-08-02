#!/usr/bin/env python3
"""Read-only, intentionally narrow structural validator for OKF v0.2."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

try:
    import yaml
    from pydantic import (
        BaseModel,
        ConfigDict,
        ValidationError,
        field_validator,
        model_validator,
    )
    from pydantic_core import PydanticCustomError
except ImportError as error:
    raise SystemExit(
        "Missing validator dependency. Run with: uv run --with pydantic --with pyyaml scripts/validate_okf.py <file-or-bundle>"
    ) from error


ROOT_LINK = re.compile(r"!?(?:\[[^\]]*\])\((/[^\s)]+)(?:\s+[^)]*)?\)")
FOOTNOTE = re.compile(r"\[\^([^\]]+)\]")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LOG_HEADING = re.compile(r"^##\s+(.+?)\s*$")
COMPUTATION_HEADING = re.compile(r"^# Computation\s*$", re.MULTILINE)


def nonempty_string(value: Any, code: str, message: str) -> str:
    """Return a usable string or raise a stable Pydantic validation error."""
    if not isinstance(value, str) or not value.strip():
        raise PydanticCustomError(code, message)
    return value


class SourceMetadata(BaseModel):
    """A provenance source with required resource and preserved extensions."""

    model_config = ConfigDict(extra="allow")

    resource: str
    id: str | None = None

    @field_validator("resource")
    @classmethod
    def resource_is_usable(cls, value: str) -> str:
        return nonempty_string(value, "source_resource_missing", "source resource is required")


class GeneratedMetadata(BaseModel):
    """Generation metadata; only the producer identity is required when present."""

    model_config = ConfigDict(extra="allow")

    by: str
    at: dt.datetime | None = None

    @field_validator("by")
    @classmethod
    def producer_is_usable(cls, value: str) -> str:
        return nonempty_string(value, "generated_by_missing", "generated.by is required")


class VerifiedEvent(BaseModel):
    """One verification event with mandatory actor and timestamp."""

    model_config = ConfigDict(extra="allow")

    by: str
    at: dt.datetime

    @field_validator("by")
    @classmethod
    def verifier_is_usable(cls, value: str) -> str:
        return nonempty_string(value, "verified_event_missing_fields", "verified.by is required")


class ConceptMetadata(BaseModel):
    """Standardized concept metadata while retaining arbitrary producer extensions."""

    model_config = ConfigDict(extra="allow")

    type: str
    title: str | None = None
    description: str | None = None
    resource: Any | None = None
    tags: Any | None = None
    sources: list[SourceMetadata] | None = None
    generated: GeneratedMetadata | None = None
    verified: VerifiedEvent | list[VerifiedEvent] | None = None
    status: Literal["draft", "stable", "deprecated"] | None = None
    stale_after: dt.date | None = None
    runtime: str | None = None
    computation: str | None = None

    @field_validator("type")
    @classmethod
    def type_is_usable(cls, value: str) -> str:
        return nonempty_string(value, "type_missing", "type is required")

    @field_validator("runtime")
    @classmethod
    def runtime_is_usable(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return nonempty_string(value, "runtime_invalid", "runtime must be a nonempty string")

    @field_validator("computation")
    @classmethod
    def computation_is_usable(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return nonempty_string(value, "computation_invalid", "computation must be a nonempty path string")

    @model_validator(mode="after")
    def validate_attested_computation(self) -> ConceptMetadata:
        if self.type == "Attested Computation" and self.runtime is None:
            raise PydanticCustomError("runtime_missing", "Attested Computation requires runtime")
        return self


@dataclass(frozen=True)
class Diagnostic:
    """A machine-readable validation finding."""

    path: str
    severity: str
    code: str
    explanation: str


class Validator:
    """Validate supplied Markdown without modifying files or executing content."""

    def __init__(self, bundle_root: Path | None, check_links: bool, is_bundle: bool) -> None:
        self.bundle_root = bundle_root.resolve() if bundle_root else None
        self.check_links = check_links
        self.is_bundle = is_bundle
        self.diagnostics: list[Diagnostic] = []

    def report(self, path: Path, severity: str, code: str, explanation: str) -> None:
        self.diagnostics.append(Diagnostic(str(path), severity, code, explanation))

    def validate(self, path: Path) -> None:
        """Validate one Markdown file according to its concept or reserved role."""
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            self.report(path, "ERROR", "FILE_UNREADABLE", f"Cannot read UTF-8 Markdown: {error}")
            return
        if path.name == "index.md":
            body = self.validate_index(path, text)
        elif path.name == "log.md":
            body = self.validate_log(path, text)
        else:
            body = self.validate_concept(path, text)
        if self.check_links:
            self.validate_root_links(path, body)

    def split_frontmatter(self, path: Path, text: str, required: bool) -> tuple[str | None, str]:
        """Extract delimited frontmatter and return it with the Markdown body."""
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            if required:
                self.report(path, "ERROR", "FRONTMATTER_OPENING", "Frontmatter must start with an opening `---` delimiter.")
            return None, text
        for index in range(1, len(lines)):
            if lines[index] == "---":
                return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
        self.report(path, "ERROR", "FRONTMATTER_CLOSING", "Frontmatter has no closing `---` delimiter.")
        return None, text

    def load_metadata(self, path: Path, frontmatter: str) -> dict[str, Any] | None:
        """Load YAML safely and require a mapping without exposing rejected values."""
        try:
            parsed = yaml.safe_load(frontmatter)
        except (yaml.YAMLError, ValueError):
            self.report(path, "ERROR", "YAML_INVALID", "Frontmatter is not valid YAML.")
            return None
        if not isinstance(parsed, dict):
            self.report(path, "ERROR", "YAML_NOT_MAPPING", "Frontmatter YAML must be a mapping.")
            return None
        return parsed

    def validate_concept(self, path: Path, text: str) -> str:
        """Validate required and standardized optional concept metadata with Pydantic."""
        frontmatter, body = self.split_frontmatter(path, text, required=True)
        if frontmatter is None:
            return body
        raw_metadata = self.load_metadata(path, frontmatter)
        if raw_metadata is None:
            return body
        try:
            metadata = ConceptMetadata.model_validate(raw_metadata)
        except ValidationError as error:
            for issue in error.errors():
                code, explanation = self.metadata_diagnostic(issue)
                self.report(path, "ERROR", code, explanation)
            if (
                raw_metadata.get("type") == "Attested Computation"
                and not self.usable_string(raw_metadata.get("computation"))
                and not COMPUTATION_HEADING.search(self.markdown_for_checks(body))
            ):
                self.report(path, "ERROR", "COMPUTATION_MISSING", "Attested Computation requires `computation` or a level-1 `# Computation` heading.")
            return body
        if (
            metadata.type == "Attested Computation"
            and metadata.computation is None
            and not COMPUTATION_HEADING.search(self.markdown_for_checks(body))
        ):
            self.report(path, "ERROR", "COMPUTATION_MISSING", "Attested Computation requires `computation` or a level-1 `# Computation` heading.")
        self.validate_source_footnotes(path, metadata, body)
        return body

    @staticmethod
    def metadata_diagnostic(issue: dict[str, Any]) -> tuple[str, str]:
        """Translate Pydantic locations/types into stable public diagnostics."""
        location = tuple(str(part) for part in issue["loc"])
        error_type = issue["type"]
        if error_type == "type_missing" or location[:1] == ("type",):
            return "TYPE_MISSING", "Concept documents require a nonempty string `type` field."
        if error_type in {"runtime_missing", "runtime_invalid"} or location[:1] == ("runtime",):
            code = "RUNTIME_MISSING" if error_type == "runtime_missing" else "RUNTIME_INVALID"
            return code, "`type: Attested Computation` requires a nonempty usable `runtime`."
        if error_type == "computation_invalid" or location[:1] == ("computation",):
            return "COMPUTATION_INVALID", "`computation` must be a nonempty usable path string."
        if location[:1] == ("sources",):
            if len(location) == 1:
                return "SOURCES_NOT_LIST", "`sources`, when present, must be a list of mappings."
            if location[-1] == "resource" or error_type == "source_resource_missing":
                return "SOURCE_RESOURCE_MISSING", "Every `sources` mapping requires a usable `resource`."
            return "SOURCE_NOT_MAPPING", "Every `sources` entry must be a mapping."
        if location[:1] == ("generated",):
            if len(location) == 1:
                return "GENERATED_NOT_MAPPING", "`generated`, when present, must be a mapping."
            if location[-1] == "at":
                return "GENERATED_AT_INVALID", "`generated.at`, when supplied, must be a parseable ISO 8601 datetime."
            return "GENERATED_BY_MISSING", "`generated.by` is required when `generated` is present."
        if location[:1] == ("verified",):
            if any(part in {"by", "at"} for part in location):
                return "VERIFIED_EVENT_MISSING_FIELDS", "Every `verified` event requires usable `by` and parseable `at`."
            return "VERIFIED_EVENT_INVALID", "`verified` must be a mapping or list of event mappings."
        if location[:1] == ("status",):
            return "STATUS_INVALID", "`status` must be `draft`, `stable`, or `deprecated`."
        if location[:1] == ("stale_after",):
            return "STALE_AFTER_INVALID", "`stale_after` must be a parseable ISO `YYYY-MM-DD` date."
        return "METADATA_INVALID", "Standardized frontmatter metadata has an invalid shape."

    def validate_source_footnotes(self, path: Path, metadata: ConceptMetadata, body: str) -> None:
        """Warn when a body footnote cannot join to a present source identifier."""
        source_ids = {source.id for source in metadata.sources or [] if source.id}
        for footnote_id in FOOTNOTE.findall(self.markdown_for_checks(body)):
            if footnote_id not in source_ids:
                self.report(path, "WARNING", "SOURCE_FOOTNOTE_UNMATCHED", f"Footnote `[^{footnote_id}]` has no matching `sources[].id`.")

    def validate_index(self, path: Path, text: str) -> str:
        """Enforce the narrow frontmatter exception for bundle-root index files."""
        frontmatter, body = self.split_frontmatter(path, text, required=False)
        if frontmatter is None:
            return body
        if not self.is_bundle or path.parent.resolve() != self.bundle_root:
            self.report(path, "ERROR", "INDEX_FRONTMATTER_NOT_ALLOWED", "Only a bundle-root `index.md` may contain frontmatter.")
            return body
        metadata = self.load_metadata(path, frontmatter)
        if metadata is not None and set(metadata) - {"okf_version"}:
            self.report(path, "ERROR", "INDEX_FRONTMATTER_KEY", "Bundle-root index frontmatter may declare only `okf_version`.")
        return body

    def validate_log(self, path: Path, text: str) -> str:
        """Check ISO date headings and newest-first order in a reserved log."""
        dates: list[dt.date] = []
        for line in self.markdown_for_checks(text).splitlines():
            match = LOG_HEADING.match(line)
            if not match:
                continue
            try:
                dates.append(dt.date.fromisoformat(match.group(1)))
            except ValueError:
                self.report(path, "ERROR", "LOG_DATE_INVALID", "Log headings must use ISO `YYYY-MM-DD` dates.")
        if any(dates[index] < dates[index + 1] for index in range(len(dates) - 1)):
            self.report(path, "ERROR", "LOG_DATES_NOT_NEWEST_FIRST", "Log date headings must be ordered newest first.")
        return text

    def validate_root_links(self, path: Path, body: str) -> None:
        """Warn for unavailable root links; relative links are intentionally ignored."""
        links = ROOT_LINK.findall(self.markdown_for_checks(body))
        if links and self.bundle_root is None:
            self.report(path, "WARNING", "ROOT_LINK_CHECK_SKIPPED", "Root-relative links were not resolved for a single file; pass `--bundle-root` to check them.")
            return
        for destination in links:
            target = destination.split("#", 1)[0].split("?", 1)[0]
            candidate = (self.bundle_root / target.lstrip("/")).resolve()  # type: ignore[operator]
            try:
                candidate.relative_to(self.bundle_root)  # type: ignore[arg-type]
            except ValueError:
                self.report(path, "WARNING", "LINK_TARGET_UNAVAILABLE", f"Bundle-root link `{destination}` escapes the bundle root.")
            else:
                if not candidate.exists():
                    self.report(path, "WARNING", "LINK_TARGET_UNAVAILABLE", f"Bundle-root link `{destination}` has no available target.")

    @staticmethod
    def markdown_for_checks(text: str) -> str:
        """Remove fenced and inline code before narrow Markdown checks (not a parser)."""
        kept: list[str] = []
        fenced = False
        marker = ""
        for line in text.splitlines():
            match = FENCE.match(line)
            if match:
                if not fenced:
                    fenced, marker = True, match.group(1)[0]
                elif match.group(1)[0] == marker:
                    fenced = False
                continue
            if not fenced:
                kept.append(INLINE_CODE.sub("", line))
        return "\n".join(kept)

    @staticmethod
    def usable_string(value: Any) -> bool:
        """Return whether a raw frontmatter value is a nonempty string."""
        return isinstance(value, str) and bool(value.strip())


def markdown_targets(target: Path) -> tuple[bool, list[Path]]:
    """Return whether target is a bundle and its Markdown files."""
    if not target.exists():
        raise ValueError("PATH_NOT_FOUND")
    if target.is_file():
        if target.suffix.lower() != ".md":
            raise ValueError("TARGET_NOT_MARKDOWN")
        return False, [target]
    if target.is_dir():
        return True, sorted(path for path in target.rglob("*") if path.is_file() and path.suffix.lower() == ".md")
    raise ValueError("TARGET_NOT_MARKDOWN")


def render(diagnostics: list[Diagnostic], json_output: bool, files_checked: int) -> None:
    """Emit diagnostics and a summary in text or JSON."""
    errors = sum(item.severity == "ERROR" for item in diagnostics)
    warnings = sum(item.severity == "WARNING" for item in diagnostics)
    summary = {"files_checked": files_checked, "errors": errors, "warnings": warnings, "valid": errors == 0}
    if json_output:
        print(json.dumps({"diagnostics": [asdict(item) for item in diagnostics], "summary": summary}, indent=2, sort_keys=True))
    else:
        for item in diagnostics:
            print(f"{item.severity} {item.code} {item.path}: {item.explanation}")
        print(f"Summary: {files_checked} file(s) checked, {errors} error(s), {warnings} warning(s); {'valid' if not errors else 'invalid'}.")


def main(argv: list[str] | None = None) -> int:
    """Run the validator CLI and return nonzero when any error was found."""
    parser = argparse.ArgumentParser(description="Read-only, narrow OKF v0.2 structural validator.")
    parser.add_argument("target", type=Path, help="One .md file or a bundle directory")
    parser.add_argument("--bundle-root", type=Path, help="Bundle root for resolving root-relative links in file mode")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON diagnostics")
    parser.add_argument("--no-link-check", action="store_false", dest="check_links", help="Skip root-relative link checks")
    parser.set_defaults(check_links=True)
    args = parser.parse_args(argv)
    try:
        is_bundle, paths = markdown_targets(args.target)
        if args.bundle_root is not None and not args.bundle_root.is_dir():
            raise ValueError("BUNDLE_ROOT_INVALID")
    except ValueError as error:
        code = str(error)
        explanations = {"PATH_NOT_FOUND": "Target path does not exist.", "TARGET_NOT_MARKDOWN": "Target must be a Markdown (.md) file or a directory.", "BUNDLE_ROOT_INVALID": "`--bundle-root` must name an existing directory."}
        render([Diagnostic(str(args.target), "ERROR", code, explanations[code])], args.json_output, 0)
        return 1
    bundle_root = args.bundle_root if args.bundle_root else (args.target if is_bundle else None)
    validator = Validator(bundle_root, args.check_links, is_bundle or args.bundle_root is not None)
    for path in paths:
        validator.validate(path)
    render(validator.diagnostics, args.json_output, len(paths))
    return 1 if any(item.severity == "ERROR" for item in validator.diagnostics) else 0


if __name__ == "__main__":
    sys.exit(main())
