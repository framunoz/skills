#!/usr/bin/env python3
"""Validate local Markdown links in the Quarto reference guides.

Run from the repository root:

    python3 skills/quarto/scripts/validate_reference_links.py

The validator is read-only and uses only the Python standard library. It checks
relative links to Markdown files and ``#anchor`` links within the current file.
External URLs, absolute paths, mailto links, and fenced code blocks are ignored.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


DEFAULT_REFERENCES_DIR = Path("skills/quarto/references")
MARKDOWN_SUFFIXES = {".md", ".markdown"}
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_PATTERN = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
EXPLICIT_ID_PATTERN = re.compile(r"\s*\{#([^}\s]+)\}\s*$")
HTML_PATTERN = re.compile(r"<[^>]+>")
INLINE_FORMATTING_PATTERN = re.compile(r"[*~`]")


@dataclass(frozen=True)
class Link:
    """A Markdown link destination and the line on which it appears."""

    destination: str
    line: int


def lines_outside_fences(path: Path) -> list[tuple[int, str]]:
    """Return file lines outside fenced code blocks."""
    active_fence: str | None = None
    result: list[tuple[int, str]] = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)
            if active_fence is None:
                active_fence = marker[0]
            elif marker[0] == active_fence:
                active_fence = None
            continue
        if active_fence is None:
            result.append((line_number, line))
    return result


def extract_links(lines: list[tuple[int, str]]) -> list[Link]:
    """Extract inline Markdown link destinations without parsing code fences."""
    links: list[Link] = []
    for line_number, line in lines:
        start = 0
        while True:
            open_index = line.find("](", start)
            if open_index == -1:
                break

            index = open_index + 2
            depth = 1
            while index < len(line) and depth:
                if line[index] == "\\":
                    index += 2
                    continue
                if line[index] == "(":
                    depth += 1
                elif line[index] == ")":
                    depth -= 1
                index += 1

            if depth:
                start = open_index + 2
                continue

            destination = line[open_index + 2 : index - 1].strip()
            if destination.startswith("<") and ">" in destination:
                destination = destination[1 : destination.index(">")]
            else:
                destination = destination.split(maxsplit=1)[0] if destination else ""
            links.append(Link(destination, line_number))
            start = index
    return links


def heading_ids(lines: list[tuple[int, str]]) -> set[str]:
    """Return explicit and GitHub-style generated identifiers for headings."""
    identifiers: set[str] = set()
    occurrences: dict[str, int] = {}
    for _, line in lines:
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        heading = match.group(2)
        explicit_id = EXPLICIT_ID_PATTERN.search(heading)
        if explicit_id:
            identifiers.add(explicit_id.group(1))
            heading = heading[: explicit_id.start()]

        slug = slugify(heading)
        if not slug:
            continue
        count = occurrences.get(slug, 0)
        occurrences[slug] = count + 1
        identifiers.add(slug if count == 0 else f"{slug}-{count}")
    return identifiers


def slugify(heading: str) -> str:
    """Create the GitHub-style anchor generated for a Markdown heading."""
    text = HTML_PATTERN.sub("", heading)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = INLINE_FORMATTING_PATTERN.sub("", text).lower().strip()
    return re.sub(r"\s+", "-", "".join(character for character in text if character.isalnum() or character.isspace() or character in "-_")).strip("-")


def is_ignored_destination(destination: str) -> bool:
    """Return whether a destination is outside this validator's local scope."""
    if not destination or destination.startswith(("/", "mailto:")):
        return True
    parsed = urlsplit(destination)
    return bool(parsed.scheme or parsed.netloc)


def validate_file(path: Path) -> list[str]:
    """Validate applicable links in one reference document."""
    lines = lines_outside_fences(path)
    anchors = heading_ids(lines)
    failures: list[str] = []

    for link in extract_links(lines):
        if is_ignored_destination(link.destination):
            continue
        parsed = urlsplit(link.destination)
        target_path = unquote(parsed.path)
        anchor = unquote(parsed.fragment)

        if not target_path:
            if anchor and anchor not in anchors:
                failures.append(f"{path}:{link.line}: anchor '#{anchor}' does not match a heading in this file")
            continue

        candidate = (path.parent / target_path).resolve()
        if Path(target_path).suffix.lower() in MARKDOWN_SUFFIXES and not candidate.is_file():
            failures.append(f"{path}:{link.line}: Markdown target '{target_path}' does not exist")
    return failures


def main() -> int:
    """Run validation and return a process-compatible exit status."""
    parser = argparse.ArgumentParser(description="Validate local links in Quarto reference Markdown files.")
    parser.add_argument(
        "--references-dir",
        type=Path,
        default=DEFAULT_REFERENCES_DIR,
        help="reference directory to validate (default: %(default)s)",
    )
    arguments = parser.parse_args()
    references_dir = arguments.references_dir
    if not references_dir.is_dir():
        print(f"error: references directory not found: {references_dir}", file=sys.stderr)
        return 2

    failures = [
        failure
        for path in sorted(references_dir.rglob("*.md"))
        for failure in validate_file(path)
    ]
    if failures:
        print("Reference link validation failed:", file=sys.stderr)
        print(*failures, sep="\n", file=sys.stderr)
        return 1

    print(f"Validated local Markdown links in {references_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
