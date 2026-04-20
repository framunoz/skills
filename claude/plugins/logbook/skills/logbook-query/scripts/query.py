#!/usr/bin/env python3
"""Query entries in a logbook with optional filters."""
import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logbook", required=True)
    parser.add_argument("--since", default=None, help="ISO date (YYYY-MM-DD), inclusive")
    parser.add_argument("--until", default=None, help="ISO date (YYYY-MM-DD), inclusive")
    parser.add_argument("--type", dest="entry_type", default=None)
    parser.add_argument("--tag", default=None, help="Substring match in tags[]")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()

    project_root = Path(args.project_root or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    lb_dir = project_root / "logbook" / args.logbook
    meta_path = lb_dir / "meta.json"
    entries_path = lb_dir / "entries.jsonl"

    if not meta_path.exists():
        print(json.dumps({"ok": False, "error": f"Logbook not found: {args.logbook}"}))
        return 10

    try:
        raw_lines = entries_path.read_text().splitlines()
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    entries = []
    warnings = []
    for i, line in enumerate(raw_lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            warnings.append(f"line {i}: {e}")

    if not entries and warnings:
        print(json.dumps({"ok": False, "error": "No entries could be parsed.", "warnings": warnings}))
        return 15

    # Apply filters
    since_date = args.since[:10] if args.since else None
    until_date = args.until[:10] if args.until else None

    filtered = []
    for e in entries:
        created = (e.get("created_at") or "")[:10]

        if since_date and created < since_date:
            continue
        if until_date and created > until_date:
            continue
        if args.entry_type and e.get("type") != args.entry_type:
            continue
        if args.tag and not any(args.tag in t for t in (e.get("tags") or [])):
            continue

        filtered.append(e)

    # Sort newest first
    filtered.sort(key=lambda e: e.get("created_at", ""), reverse=True)

    # Apply limit
    if args.limit is not None:
        filtered = filtered[:args.limit]

    result: dict = {
        "ok": True,
        "logbook": args.logbook,
        "count": len(filtered),
        "entries": filtered,
    }
    if warnings:
        result["warnings"] = warnings

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
