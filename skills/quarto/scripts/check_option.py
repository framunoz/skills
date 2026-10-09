# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Look up Quarto YAML options in the schemas bundled with the installed Quarto.

Usage: uv run scripts/check_option.py <option> [<option> ...]

For each option prints: schema file, formats it applies to, whether it is hidden
(hidden usually means deprecated or internal), allowed values, and description.
Unknown options get close-match suggestions. The schemas ship with Quarto, so the
answer always matches the installed version (`quarto --version`).
"""

import difflib
import subprocess
import sys
from pathlib import Path

import yaml


def schema_dir() -> Path:
    out = subprocess.run(["quarto", "--paths"], capture_output=True, text=True, check=True)
    share = out.stdout.strip().splitlines()[-1]
    return Path(share) / "schema"


def load_entries(root: Path) -> dict[str, list[tuple[str, dict]]]:
    entries: dict[str, list[tuple[str, dict]]] = {}
    for f in sorted(root.glob("*.yml")):
        if not f.name.startswith(("document-", "cell-", "project")):
            continue
        data = yaml.safe_load(f.read_text()) or []
        if not isinstance(data, list):
            continue
        for item in data:
            if isinstance(item, dict) and "name" in item:
                entries.setdefault(item["name"], []).append((f.name, item))
    return entries


def describe(value) -> str:
    if isinstance(value, dict):
        value = value.get("short") or value.get("long") or ""
    return " ".join(str(value).split())


def completions(schema) -> list[str]:
    found: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("enum", "completions") and isinstance(v, list):
                    found.extend(str(x) for x in v)
                elif k == "enum" and isinstance(v, dict) and isinstance(v.get("values"), list):
                    found.extend(str(x) for x in v["values"])
                else:
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(schema)
    return list(dict.fromkeys(found))


def nested_hits(name: str) -> list[str]:
    import re

    pat = re.compile(rf"^\s+{re.escape(name)}:", re.M)
    return [f.name for f in sorted(schema_dir().glob("*.yml")) if pat.search(f.read_text())]


def main(names: list[str]) -> int:
    entries = load_entries(schema_dir())
    missing = 0
    for name in names:
        print(f"== {name}")
        if name not in entries:
            nested = nested_hits(name)
            if nested:
                print(f"   nested property (not top-level) in: {', '.join(nested)}")
                print("   inspect with: grep -n -A10 '  " + name + ":' " + str(schema_dir()) + "/<file>")
                continue
            missing += 1
            close = difflib.get_close_matches(name, entries.keys(), n=5, cutoff=0.6)
            print("   NOT FOUND in bundled schemas." + (f" Did you mean: {', '.join(close)}" if close else ""))
            continue
        for fname, item in entries[name]:
            tags = item.get("tags") or {}
            formats = tags.get("formats")
            vals = completions(item.get("schema"))
            print(f"   file:     {fname}")
            if item.get("hidden"):
                print("   hidden:   yes (deprecated or internal; prefer the documented alternative)")
            if formats:
                print(f"   formats:  {', '.join(map(str, formats))}")
            if vals:
                print(f"   values:   {', '.join(vals[:25])}{' ...' if len(vals) > 25 else ''}")
            print(f"   desc:     {describe(item.get('description'))[:300]}")
    return 1 if missing else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
