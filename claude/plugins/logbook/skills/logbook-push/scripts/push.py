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


def _get_existing_data(entries_path: Path) -> tuple[dict[int, str], int]:
    """Return ({id -> ulid}, next_id) for all existing entries."""
    ids: dict[int, str] = {}
    max_id = 0
    if not entries_path.exists():
        return ids, 1
    try:
        with entries_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    eid = entry.get("id", 0)
                    ids[eid] = entry.get("ulid", "")
                    if eid > max_id:
                        max_id = eid
                except (json.JSONDecodeError, KeyError):
                    pass
    except OSError:
        pass
    return ids, max_id + 1


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
        meta_path.read_text()  # verify meta.json is readable
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON on stdin: {e}"}))
        return 11

    # Schema validation
    existing_ids, next_id = _get_existing_data(entries_path)

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
        error_msg = "; ".join(errors)
        if args.entry_type == "amendment" and any("does not exist" in e or "does not match" in e for e in errors):
            print(json.dumps({"ok": False, "error": error_msg}))
            return 13
        print(json.dumps({"ok": False, "error": error_msg}))
        return 11

    # Sensitive content scan
    if not args.acknowledge_sensitive:
        hits = _schemas.scan_sensitive(payload)
        if hits:
            print(json.dumps({"ok": False, "error": "Sensitive content detected. Re-invoke with --acknowledge-sensitive.", "patterns": hits}))
            return 14

    try:
        ulid = _make_ulid()
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        entry = {"id": next_id, "ulid": ulid, "created_at": created_at, "type": args.entry_type}
        entry.update(payload)
        # Ensure server-assigned fields override anything in payload
        entry["id"] = next_id
        entry["ulid"] = ulid
        entry["created_at"] = created_at
        entry["type"] = args.entry_type

        if entries_path.exists() and entries_path.stat().st_size > 0:
            with entries_path.open("rb+") as f_check:
                f_check.seek(-1, os.SEEK_END)
                if f_check.read(1) != b"\n":
                    f_check.write(b"\n")

        with entries_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 99

    rel_path = f"logbook/{args.logbook}/entries.jsonl"
    result = {"ok": True, "id": next_id, "ulid": ulid, "logbook": args.logbook, "path": rel_path}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
