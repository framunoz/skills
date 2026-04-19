#!/usr/bin/env python3
"""Create a new logbook: directory, meta.json, empty entries.jsonl."""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SLUG_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
VALID_TYPES = {"tests", "collaboration", "free"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logbook", required=True)
    parser.add_argument("--type", dest="schema_type", required=True)
    parser.add_argument("--title", default=None)
    parser.add_argument("--description", default="")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()

    if not SLUG_RE.match(args.logbook):
        print(json.dumps({"ok": False, "error": f"Invalid slug: {args.logbook!r}"}))
        return 16

    if args.schema_type not in VALID_TYPES:
        print(json.dumps({"ok": False, "error": f"Invalid type: {args.schema_type!r}. Must be one of {sorted(VALID_TYPES)}."}))
        return 18

    project_root = Path(args.project_root or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    lb_dir = project_root / "logbook" / args.logbook

    if lb_dir.exists():
        print(json.dumps({"ok": False, "error": f"Logbook already exists: {lb_dir}"}))
        return 17

    try:
        lb_dir.mkdir(parents=True)
        meta = {
            "slug": args.logbook,
            "schema_type": args.schema_type,
            "title": args.title if args.title is not None else args.logbook,
            "description": args.description,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "format_version": 1,
        }
        (lb_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        (lb_dir / "entries.jsonl").write_text("")
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    rel_path = f"logbook/{args.logbook}/"
    print(json.dumps({"ok": True, "logbook": args.logbook, "path": rel_path, "schema_type": args.schema_type}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
