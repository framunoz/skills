import itertools
import pathlib
import re
import sys


def check_anti_patterns(directory="src"):
    """Scans for Kedro anti-patterns in Python files."""
    anti_patterns = {
        r"\.to_csv\(": (
            "Direct I/O (.to_csv) detected in node. Use the Data Catalog instead."
        ),
        r"\.to_parquet\(": (
            "Direct I/O (.to_parquet) detected in node. Use the Data Catalog instead."
        ),
        r"\.savefig\(": (
            "Direct I/O (.savefig) detected in node. Use the Data Catalog instead."
        ),
        r"from kedro\.pipeline\.modular_pipeline import node": (
            "Deprecated 'node' wrapper import. Use 'from kedro.pipeline import Node'."
        ),
        r"from kedro\.pipeline\.modular_pipeline import pipeline": (
            "Deprecated 'pipeline' wrapper import. Use 'from kedro.pipeline import"
            " Pipeline'."
        ),
        r"DataSet": "Old 'DataSet' naming convention. Use 'Dataset' (lowercase 's').",
    }

    found_issues = []
    base_dir = pathlib.Path(directory)

    # Scans for Python and YAML files using rglob
    for path in base_dir.rglob("*"):
        if not path.is_file() or path.suffix not in (".py", ".yml"):
            continue

        try:
            with path.open(encoding="utf-8") as f:
                for (i, line), (pattern, message) in itertools.product(
                    enumerate(f, 1), anti_patterns.items()
                ):
                    if re.search(pattern, line):
                        found_issues.append(f"{path}:{i}: {message}")
        except Exception as e:
            print(f"Error reading {path}: {e}")  # noqa: T201

    return found_issues


if __name__ == "__main__":
    issues = check_anti_patterns()
    if issues:
        print("Kedro Validation Failed:")  # noqa: T201
        for issue in issues:
            print(f"  - {issue}")  # noqa: T201
        sys.exit(1)
    else:
        print("Kedro Validation Passed: No obvious anti-patterns found.")  # noqa: T201
        sys.exit(0)
