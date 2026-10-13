#!/usr/bin/env python3
"""Read-only Kedro preflight: interpreter, versions vs. this skill, project facts, stale-pattern lint.

Run with the PROJECT's interpreter (stdlib only):
    uv run python <skill>/scripts/kedro_preflight.py [--project PATH]

Never imports project code, runs pipelines, or writes files. Exit code 1 when Kedro is missing
or a blocking problem is found (major-version mismatch, secrets under conf/base).
"""

from __future__ import annotations

import argparse
import importlib.metadata as md
import os
import re
import sys
from pathlib import Path

SKILL_KEDRO_VERSION = "1.7.0"
PACKAGES = ["kedro", "kedro-datasets", "kedro-viz", "kedro-telemetry", "omegaconf", "pydantic", "pandera"]
SKIP = {".venv", "venv", ".git", "node_modules", "__pycache__", "build", "dist", ".ipynb_checkpoints"}

# (regex, where, message) — patterns that were valid before Kedro 1.x / kedro-datasets 2.x
STALE = [
    (r"kedro\.extras\.datasets", "py,yml", "kedro.extras.datasets was removed (0.19) -> kedro-datasets"),
    (r"\b\w+DataSet\b", "py,yml", "old `DataSet` casing -> `Dataset` (kedro-datasets 2.0)"),
    (r"\b(TemplatedConfigLoader|ConfigLoader)\b(?<!OmegaConfigLoader)", "py", "only OmegaConfigLoader exists since 0.19"),
    (r"^\s{2}layer:", "catalog", "top-level `layer:` is gone -> metadata: {kedro-viz: {layer: ...}}"),
    (r"KedroDataCatalog", "py", "KedroDataCatalog was renamed DataCatalog (1.0)"),
    (r"kedro\.pipeline\.modular_pipeline|ModularPipelineError", "py", "modular_pipeline module removed (1.0) -> kedro.pipeline / PipelineError"),
    (r"RUNNER_MODULES_WHITELIST", "py", "renamed RUNNER_MODULE_ALLOWLIST (1.6)"),
    (r"--namespace\b(?!s)", "py,sh,yml,md,toml", "`kedro run --namespace` removed (1.0) -> --namespaces"),
    (r"kedro run\b.*--pipeline(?!s)[ =]", "py,sh,yml,md,toml", "`kedro run --pipeline` deprecated (1.7) -> --pipelines"),
    (r"kedro catalog (list|rank|resolve|create)\b", "py,sh,md", "catalog CLI renamed (1.0): describe-datasets / list-patterns / resolve-patterns"),
    (r"\bsession_id\b", "py", "session_id renamed run_id in runners and hooks (1.0)"),
    (r"\bextra_params\b", "py", "extra_params renamed runtime_params (1.0)"),
    (r"\.add_feed_dict\(|catalog\.list\(\)|\.shallow_copy\(\)|\.add_all\(", "py", "DataCatalog method removed (1.0)"),
]


def version_of(name: str) -> str | None:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return None


def parse(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def compare(installed: str, skill: str = SKILL_KEDRO_VERSION) -> str:
    a, b = parse(installed), parse(skill)
    if a == b:
        return "same as skill"
    if a > b:
        return "NEWER than skill: read RELEASE.md for the versions in between; verify APIs before use"
    return "OLDER than skill: features listed with a newer version (e.g. 1.6 dataset validation) may be missing"


def find_project(path: Path) -> Path | None:
    for d in (path.resolve(), *path.resolve().parents):
        f = d / "pyproject.toml"
        if f.is_file() and "[tool.kedro]" in f.read_text(encoding="utf-8", errors="replace"):
            return d
    return None


def tool_kedro(pyproject: Path) -> dict[str, str]:
    text = pyproject.read_text(encoding="utf-8", errors="replace")
    block = re.search(r"^\[tool\.kedro\]\s*\n(.*?)(?=^\[|\Z)", text, re.M | re.S)
    out = {}
    for line in (block.group(1) if block else "").splitlines():
        m = re.match(r'\s*([\w-]+)\s*=\s*"?(.*?)"?\s*$', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def files(root: Path, exts: set[str]) -> list[Path]:
    """Source/config files, pruning envs, VCS and the data/ tree (can be huge)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".") and not (rel == Path(".") and d == "data")]
        out += [Path(dirpath) / f for f in filenames if f.rsplit(".", 1)[-1] in exts]
    return out


def lint(root: Path) -> list[str]:
    found = []
    cache: dict[str, list[Path]] = {}
    for pattern, where, message in STALE:
        if where == "catalog":
            targets = [p for p in (root / "conf").rglob("catalog*.y*ml")] if (root / "conf").is_dir() else []
        else:
            exts = set(where.split(","))
            key = ",".join(sorted(exts))
            targets = cache.setdefault(key, files(root, exts))
        regex = re.compile(pattern, re.M)
        for path in targets:
            if path.name == Path(__file__).name:
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if regex.search(line):
                    found.append(f"{path.relative_to(root)}:{lineno}: {message}")
                    break  # one hit per file per pattern is enough
    return found


# Direct I/O inside node modules bypasses the catalog (no versioning, no Viz lineage, no
# --only-missing-outputs, untestable without files). Checked only in pipelines/*/nodes*.py.
NODE_IO = re.compile(
    r"\.(to_csv|to_parquet|to_excel|to_json|to_pickle|to_netcdf|savefig|write_html)\(|"
    r"\bpd\.read_\w+\(|\bxr\.open_dataset\(|\bpickle\.(dump|load)\(|\bjoblib\.(dump|load)\(|\bopen\("
)


def node_io(root: Path, source_dir: str) -> list[str]:
    hits = []
    for path in sorted(root.glob(f"{source_dir}/*/pipelines/**/nodes*.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            code = line.split("#", 1)[0]
            if NODE_IO.search(code):
                hits.append(f"{path.relative_to(root)}:{lineno}: direct I/O in a node -> declare a catalog dataset")
    return hits


def project_report(root: Path, kedro_version: str | None) -> tuple[list[str], bool]:
    lines, blocking = [], False
    meta = tool_kedro(root / "pyproject.toml")
    lines.append(f"project root: {root}")
    lines.append(f"package: {meta.get('package_name', '?')}  source_dir: {meta.get('source_dir', 'src')}  "
                 f"tools: {meta.get('tools', '-')}  example_pipeline: {meta.get('example_pipeline', '-')}")
    init = meta.get("kedro_init_version")
    if init and kedro_version:
        same_major = parse(init)[0] == parse(kedro_version)[0]
        lines.append(f"kedro_init_version: {init} (installed {kedro_version})"
                     + ("" if same_major else "  <- MAJOR MISMATCH: Kedro refuses to run; migrate or pin kedro"))
        blocking |= not same_major
    conf = root / "conf"
    if conf.is_dir():
        envs = sorted(p.name for p in conf.iterdir() if p.is_dir())
        lines.append(f"conf environments: {', '.join(envs) or 'none'}")
        for env in envs:
            names = sorted(str(p.relative_to(conf / env)) for p in (conf / env).rglob("*.y*ml"))
            lines.append(f"  {env}: {', '.join(names) or '(empty)'}")
        secrets = [p for p in (conf / "base").rglob("credentials*.y*ml")] if (conf / "base").is_dir() else []
        if secrets:
            blocking = True
            lines.append(f"SECRETS IN conf/base: {', '.join(str(p.relative_to(root)) for p in secrets)} -> move to conf/local")
        gitignore = root / ".gitignore"
        if gitignore.is_file() and "conf/local" not in gitignore.read_text(encoding="utf-8", errors="replace"):
            lines.append("warning: .gitignore does not mention conf/local (credentials may be committed)")
    else:
        lines.append("conf/: missing (or a custom CONF_SOURCE in settings.py)")
    settings = next(iter(root.glob(f"{meta.get('source_dir', 'src')}/*/settings.py")), None)
    if settings:
        text = settings.read_text(encoding="utf-8", errors="replace")
        active = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
        for key in ("CONFIG_LOADER_ARGS", "HOOKS", "DATA_CATALOG_CLASS", "CONF_SOURCE", "SESSION_CLASS"):
            if re.search(rf"^{key}\s*=", active, re.M):
                lines.append(f"settings.py sets {key}")
        if "merge_strategy" in active:
            lines.append("settings.py: custom merge_strategy present (check soft vs destructive)")
    for marker in ("uv.lock", "requirements.txt", ".venv"):
        if (root / marker).exists():
            lines.append(f"found {marker}")
    if (root / "requirements.txt").exists() and (root / "uv.lock").exists():
        lines.append("note: both requirements.txt and uv.lock — keep pyproject.toml as the source of truth")
    return lines, blocking


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Kedro preflight.")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args()

    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"interpreter: {sys.executable} ({'virtualenv' if in_venv else 'NOT a virtualenv: probably not the project env'})")
    versions = {name: version_of(name) for name in PACKAGES}
    print("versions: " + ", ".join(f"{k} {v}" for k, v in versions.items() if v))
    status = 0
    kedro_version = versions["kedro"]
    if kedro_version is None:
        print("kedro: NOT installed in this interpreter -> use the project env (`uv run python ...`)")
        status = 1
    else:
        print(f"skill written for kedro {SKILL_KEDRO_VERSION} -> {compare(kedro_version)}")

    root = find_project(args.project)
    if root is None:
        print(f"project: none (no pyproject.toml with [tool.kedro] at or above {args.project.resolve()})")
        return status
    lines, blocking = project_report(root, kedro_version)
    print(*lines, sep="\n")
    stale = lint(root) + node_io(root, tool_kedro(root / "pyproject.toml").get("source_dir", "src"))
    print("stale patterns:" if stale else "stale patterns: none")
    for item in stale[:40]:
        print(f"  {item}")
    if len(stale) > 40:
        print(f"  ... {len(stale) - 40} more")
    return 1 if (status or blocking) else 0


if __name__ == "__main__":
    sys.exit(main())
