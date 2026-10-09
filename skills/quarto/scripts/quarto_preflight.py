#!/usr/bin/env python3
"""Read-only Quarto preflight: installed version vs. this skill, and project facts.

Usage:
    python3 scripts/quarto_preflight.py [--project PATH] [--quarto EXECUTABLE]

Reports the Quarto executable and version, compares it with the version this skill was
written against, and — given a path — the project root and the files that shape the
effective configuration and the execution environment. Standard library only. It never
renders, executes document code, modifies files, or installs anything.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_QUARTO_VERSION = "1.10.19"
SKIP_DIRS = {".git", ".quarto", "_freeze", "_site", "_book", "_output", "node_modules", ".venv", "renv"}


def parse_version(text: str) -> tuple[int, ...] | None:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", text)
    return tuple(int(part) for part in match.groups()) if match else None


def compare_versions(installed: str, skill: str = SKILL_QUARTO_VERSION) -> str:
    current, written = parse_version(installed), parse_version(skill)
    if current is None or written is None:
        return "unknown (could not parse version)"
    if current == written:
        return "same as skill"
    if current > written:
        return "NEWER than skill: verify options with check_option.py and read the changelog"
    return "OLDER than skill: features from newer releases may be missing"


def find_project_root(path: Path) -> Path | None:
    """Return the nearest ancestor containing ``_quarto.yml``, if any."""
    candidate = path.resolve()
    if candidate.is_file():
        candidate = candidate.parent
    for directory in (candidate, *candidate.parents):
        if (directory / "_quarto.yml").is_file():
            return directory
    return None


def walk(root: Path, pattern: str) -> list[Path]:
    return sorted(
        item for item in root.rglob(pattern)
        if not any(part in SKIP_DIRS for part in item.relative_to(root).parts[:-1])
    )


def project_type(config: Path) -> str:
    text = config.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"^project:\s*\n(?:[ \t]+.*\n)*?[ \t]+type:\s*([\w-]+)", text, re.M)
    return match.group(1) if match else "default"


def inspect_project(path: Path) -> list[str]:
    root = find_project_root(path)
    if root is None:
        start = path.resolve() if path.is_dir() else path.resolve().parent
        return [
            f"project: none (no _quarto.yml above {path.resolve()})",
            "note: without _quarto.yml, R starts in the shell's cwd, so a root .Rprofile/renv "
            "is only loaded when quarto runs from that directory",
            *environment_facts(start),
        ]
    rel = lambda items: ", ".join(str(i.relative_to(root)) for i in items) or "none"
    documents = walk(root, "*.qmd") + walk(root, "*.ipynb")
    return [
        f"project root: {root}",
        f"project type: {project_type(root / '_quarto.yml')}",
        f"profiles: {rel(sorted(root.glob('_quarto-*.yml')))}",
        f"local overrides: {rel(sorted(root.glob('_quarto.yml.local')))}",
        f"directory metadata: {rel(walk(root, '_metadata.yml'))}",
        f"brand: {rel(sorted(root.glob('_brand.yml')) + sorted(root.glob('_brand/')))}",
        f"extensions: {rel(sorted((root / '_extensions').glob('*/*')) if (root / '_extensions').is_dir() else [])}",
        f"frozen results: {'_freeze/ present' if (root / '_freeze').is_dir() else 'none'}",
        f"documents: {len(documents)} (.qmd/.ipynb)",
        *environment_facts(root),
    ]


ENV_MARKERS = {
    ".venv": "python env: {} -> run `uv run quarto ...` or set QUARTO_PYTHON",
    "pyproject.toml": "python project: {}",
    "renv.lock": "r env: {}",
    ".Rprofile": "r profile: {} (activates renv when R starts in that directory)",
}


def environment_facts(root: Path, levels: int = 3) -> list[str]:
    """Report environment files at the root or up to ``levels`` ancestors (nearest wins)."""
    facts = []
    for marker, template in ENV_MARKERS.items():
        for directory in (root, *root.parents[:levels]):
            if (directory / marker).exists():
                facts.append(template.format(directory / marker))
                break
    return facts or ["environment files: none found near the project"]


def quarto_version(executable: str) -> tuple[int, str]:
    try:
        result = subprocess.run([executable, "--version"], check=False, capture_output=True, text=True)
    except OSError as error:
        return 1, f"unable to run --version: {error}"
    output = (result.stdout or result.stderr).strip()
    return result.returncode, output or "no version output"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Quarto preflight.")
    parser.add_argument("--quarto", default="quarto", help="Quarto executable (default: %(default)s).")
    parser.add_argument("--project", type=Path, help="Project directory or a path inside it.")
    args = parser.parse_args()

    executable = shutil.which(args.quarto) or (args.quarto if Path(args.quarto).is_file() else None)
    status = 0
    if executable is None:
        print(f"quarto executable: not found ({args.quarto}) — install Quarto; do not fabricate renders")
        status = 1
    else:
        status, version = quarto_version(executable)
        print(f"quarto executable: {executable}")
        print(f"quarto version: {version}")
        print(f"skill written for: {SKILL_QUARTO_VERSION} -> {compare_versions(version)}")

    if args.project is not None:
        if not args.project.exists():
            parser.error(f"project path does not exist: {args.project}")
        print(*inspect_project(args.project), sep="\n")
    return status


if __name__ == "__main__":
    sys.exit(main())
