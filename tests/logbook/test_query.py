#!/usr/bin/env python3
"""Tests for logbook-query (query.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import QUERY_SCRIPT


def run_query(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(QUERY_SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd)
    )


def make_logbook(tmp_path: Path, slug: str, entries: list[dict]) -> Path:
    lb_dir = tmp_path / "logbook" / slug
    lb_dir.mkdir(parents=True)
    meta = {"slug": slug, "title": slug,
            "description": "", "created_at": "2026-04-01T00:00:00Z", "format_version": 1}
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    (lb_dir / "entries.jsonl").write_text(
        "\n".join(json.dumps(e) for e in entries) + "\n"
    )
    return tmp_path


ENTRIES = [
    {"id": 1, "ulid": "A1", "created_at": "2026-04-10T10:00:00Z", "type": "tests",
     "title": "E1", "went_well": ["ok"], "went_wrong": [], "tags": ["auth"]},
    {"id": 2, "ulid": "A2", "created_at": "2026-04-12T10:00:00Z", "type": "tests",
     "title": "E2", "went_well": ["ok"], "went_wrong": [], "tags": ["perf"]},
    {"id": 3, "ulid": "A3", "created_at": "2026-04-14T10:00:00Z", "type": "tests",
     "title": "E3", "went_well": ["ok"], "went_wrong": [], "tags": ["auth", "perf"]},
    {"id": 4, "ulid": "A4", "created_at": "2026-04-16T10:00:00Z", "type": "amendment",
     "title": "Amend #1", "amends": {"id": 1, "ulid": "A1"}, "reason": "Typo", "body": "fix"},
    {"id": 5, "ulid": "A5", "created_at": "2026-04-18T10:00:00Z", "type": "tests",
     "title": "E5", "went_well": ["ok"], "went_wrong": [], "tags": []},
]


def test_since_filter(tmp_path):
    make_logbook(tmp_path, "q1", ENTRIES)
    result = run_query(["--logbook", "q1", "--since", "2026-04-13", "--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    ids = [e["id"] for e in out["entries"]]
    assert 1 not in ids
    assert 2 not in ids
    assert 3 in ids


def test_until_filter(tmp_path):
    make_logbook(tmp_path, "q2", ENTRIES)
    result = run_query(["--logbook", "q2", "--until", "2026-04-11", "--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    ids = [e["id"] for e in out["entries"]]
    assert 1 in ids
    assert 2 not in ids


def test_type_filter(tmp_path):
    make_logbook(tmp_path, "q3", ENTRIES)
    result = run_query(["--logbook", "q3", "--type", "amendment", "--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    assert all(e["type"] == "amendment" for e in out["entries"])


def test_tag_filter(tmp_path):
    make_logbook(tmp_path, "q4", ENTRIES)
    result = run_query(["--logbook", "q4", "--tag", "auth", "--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    for e in out["entries"]:
        assert "auth" in (e.get("tags") or [])


def test_limit(tmp_path):
    make_logbook(tmp_path, "q5", ENTRIES)
    result = run_query(["--logbook", "q5", "--limit", "2", "--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    assert len(out["entries"]) <= 2


def test_zero_match_returns_count_0(tmp_path):
    make_logbook(tmp_path, "q6", ENTRIES)
    result = run_query(["--logbook", "q6", "--since", "2030-01-01", "--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["count"] == 0
    assert out["entries"] == []


def test_corrupt_line_skipped_exit_0(tmp_path):
    lb_dir = tmp_path / "logbook" / "q7"
    lb_dir.mkdir(parents=True)
    meta = {"slug": "q7", "title": "q7",
            "description": "", "created_at": "2026-04-01T00:00:00Z", "format_version": 1}
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    good = ENTRIES[0]
    (lb_dir / "entries.jsonl").write_text(json.dumps(good) + "\nBAD_LINE\n")
    result = run_query(["--logbook", "q7", "--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["count"] >= 1
    assert "warnings" in out


def test_logbook_not_found_exits_10(tmp_path):
    result = run_query(["--logbook", "nonexistent", "--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 10


def test_results_ordered_newest_first(tmp_path):
    make_logbook(tmp_path, "q8", ENTRIES)
    result = run_query(["--logbook", "q8", "--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    dates = [e["created_at"] for e in out["entries"]]
    assert dates == sorted(dates, reverse=True)
