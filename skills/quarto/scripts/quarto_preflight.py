#!/usr/bin/env python3
"""Report Quarto availability and inspect a project without rendering.

Examples:
    python3 skills/quarto/scripts/quarto_preflight.py
    python3 skills/quarto/scripts/quarto_preflight.py --project path/to/project

The script uses only the Python standard library. It invokes ``quarto --version``
when an executable is available, and otherwise reads project files only. It never
renders, executes document code, modifies files, or installs dependencies.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root(path: Path) -> Path | None:
    """Return the nearest ancestor containing ``_quarto.yml``, if any."""
    candidate = path.resolve()
    if candidate.is_file():
        candidate = candidate.parent

    for directory in (candidate, *candidate.parents):
        if (directory / "_quarto.yml").is_file():
            return directory
    return None


def quarto_version(executable: str) -> tuple[int, str]:
    """Run the non-mutating version command and return its status and output."""
    try:
        result = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return 1, f"unable to run --version: {error}"
    output = (result.stdout or result.stderr).strip()
    return result.returncode, output or "no version output"


def inspect_project(path: Path) -> list[str]:
    """Return read-only project facts for a supplied project or descendant path."""
    root = find_project_root(path)
    if root is None:
        return [f"project: no _quarto.yml found above {path.resolve()}"]

    profiles = sorted(item.name for item in root.glob("_quarto-*.yml"))
    metadata_files = sorted(
        str(item.relative_to(root)) for item in root.rglob("_metadata.yml")
    )
    documents = sorted(
        str(item.relative_to(root))
        for pattern in ("*.qmd", "*.ipynb")
        for item in root.rglob(pattern)
    )
    return [
        f"project root: {root}",
        "project config: _quarto.yml",
        f"profiles: {', '.join(profiles) if profiles else 'none'}",
        f"directory metadata: {', '.join(metadata_files) if metadata_files else 'none'}",
        f"documents: {len(documents)} (.qmd/.ipynb)",
    ]


def main() -> int:
    """Parse arguments, report Quarto status, and optionally inspect a project."""
    parser = argparse.ArgumentParser(
        description="Read-only Quarto executable and project preflight."
    )
    parser.add_argument(
        "--quarto",
        default="quarto",
        help="Quarto executable name or path (default: %(default)s).",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="Project directory or a path within it to inspect without rendering.",
    )
    arguments = parser.parse_args()

    executable = shutil.which(arguments.quarto)
    if executable is None and Path(arguments.quarto).is_file():
        executable = arguments.quarto

    status = 0
    if executable is None:
        print(f"quarto executable: not found ({arguments.quarto})")
        status = 1
    else:
        version_status, version = quarto_version(executable)
        print(f"quarto executable: {executable}")
        print(f"quarto version: {version}")
        status = version_status

    if arguments.project is not None:
        if not arguments.project.exists():
            parser.error(f"project path does not exist: {arguments.project}")
        print(*inspect_project(arguments.project), sep="\n")

    return status


if __name__ == "__main__":
    sys.exit(main())
