#!/usr/bin/env python3
"""Append one validated entry to a logbook's entries.jsonl."""
import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Locate _schemas.py relative to this script
sys.path.insert(0, str(Path(__file__).parent))
import _schemas

VALID_TYPES = {"tests", "collaboration", "free", "amendment"}


def _make_ulid() -> str:
    """Generate a ULID using time.time_ns() + uuid4 random bytes, Crockford base-32."""
    ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    ts_ms = time.time_ns() // 1_000_000
    rand_bytes = uuid.uuid4().bytes[:10]
    # 10-char timestamp part (48 bits)
    ts_chars = []
    v = ts_ms
    for _ in range(10):
        ts_chars.append(ENCODING[v & 0x1F])
        v >>= 5
    ts_part = "".join(reversed(ts_chars))
    # 16-char random part (80 bits = 10 bytes)
    rand_chars = []
    rand_int = int.from_bytes(rand_bytes, "big")
    for _ in range(16):
        rand_chars.append(ENCODING[rand_int & 0x1F])
        rand_int >>= 5
    rand_part = "".join(reversed(rand_chars))
    return ts_part + rand_part


def _read_existing_ids(entries_path: Path) -> dict:
    """Return {id -> ulid} for all existing entries."""
    result = {}
    try:
        for line in entries_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                result[entry["id"]] = entry["ulid"]
            except (json.JSONDecodeError, KeyError):
                pass
    except OSError:
        pass
    return result


def _next_id(entries_path: Path) -> int:
    """Compute next monotonic id from last non-empty line."""
    try:
        lines = [l.strip() for l in entries_path.read_text().splitlines() if l.strip()]
        if not lines:
            return 1
        last = json.loads(lines[-1])
        return last["id"] + 1
    except (OSError, json.JSONDecodeError, KeyError):
        return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logbook", required=True)
    parser.add_argument("--type", dest="entry_type", required=True)
    parser.add_argument("--acknowledge-sensitive", action="store_true")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()

    if args.entry_type not in VALID_TYPES:
        print(json.dumps({"ok": False, "error": f"Unknown type: {args.entry_type!r}"}))
        return 99

    project_root = Path(args.project_root or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    lb_dir = project_root / "logbook" / args.logbook
    meta_path = lb_dir / "meta.json"
    entries_path = lb_dir / "entries.jsonl"

    if not meta_path.exists():
        print(json.dumps({"ok": False, "error": f"Logbook not found: {args.logbook}"}))
        return 10

    try:
        meta = json.loads(meta_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    schema_type = meta.get("schema_type", "")

    # Type mismatch check (amendment always allowed)
    if args.entry_type != "amendment" and args.entry_type != schema_type:
        print(json.dumps({"ok": False, "error": f"Type mismatch: logbook is '{schema_type}', got '{args.entry_type}'"}))
        return 12

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON on stdin: {e}"}))
        return 11

    # Schema validation
    existing_ids = _read_existing_ids(entries_path)

    if args.entry_type == "tests":
        ok, errors = _schemas.validate_tests(payload)
    elif args.entry_type == "collaboration":
        ok, errors = _schemas.validate_collaboration(payload)
    elif args.entry_type == "free":
        ok, errors = _schemas.validate_free(payload)
    elif args.entry_type == "amendment":
        ok, errors = _schemas.validate_amendment(payload, existing_ids)
    else:
        ok, errors = False, [f"Unknown type: {args.entry_type}"]

    if not ok:
        if args.entry_type == "amendment" and any("does not exist" in e or "does not match" in e for e in errors):
            print(json.dumps({"ok": False, "error": errors}))
            return 13
        print(json.dumps({"ok": False, "error": errors}))
        return 11

    # Sensitive content scan
    if not args.acknowledge_sensitive:
        hits = _schemas.scan_sensitive(payload)
        if hits:
            print(json.dumps({"ok": False, "error": "Sensitive content detected. Re-invoke with --acknowledge-sensitive.", "patterns": hits}))
            return 14

    try:
        next_id = _next_id(entries_path)
        ulid = _make_ulid()
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        entry = {"id": next_id, "ulid": ulid, "created_at": created_at, "type": args.entry_type}
        entry.update(payload)
        # Ensure server-assigned fields override anything in payload
        entry["id"] = next_id
        entry["ulid"] = ulid
        entry["created_at"] = created_at
        entry["type"] = args.entry_type

        with entries_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 99

    rel_path = f"logbook/{args.logbook}/entries.jsonl"
    print(json.dumps({"ok": True, "id": next_id, "ulid": ulid, "logbook": args.logbook, "path": rel_path}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
