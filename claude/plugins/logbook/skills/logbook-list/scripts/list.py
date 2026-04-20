#!/usr/bin/env python3
"""List all logbooks in the current project."""
import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()

    project_root = Path(args.project_root or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    logbook_root = project_root / "logbook"

    if not logbook_root.exists():
        print(json.dumps({"ok": True, "logbooks": []}))
        return 0

    logbooks = []
    try:
        for entry in sorted(logbook_root.iterdir()):
            if not entry.is_dir():
                continue
            meta_path = entry / "meta.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text())
            except (json.JSONDecodeError, OSError):
                continue

            entries_path = entry / "entries.jsonl"
            entry_count = 0
            last_entry_at = None
            if entries_path.exists():
                try:
                    with entries_path.open("r", encoding="utf-8") as f:
                        last_line = None
                        count = 0
                        for line in f:
                            if line.strip():
                                last_line = line
                                count += 1
                        entry_count = count
                        if last_line:
                            try:
                                last_entry_at = json.loads(last_line).get("created_at")
                            except json.JSONDecodeError:
                                pass
                except OSError:
                    pass

            logbooks.append({
                "slug": meta.get("slug", entry.name),
                "entries": entry_count,
                "last_entry_at": last_entry_at,
            })
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    logbooks.sort(key=lambda lb: lb.get("last_entry_at") or "", reverse=True)
    print(json.dumps({"ok": True, "logbooks": logbooks}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
