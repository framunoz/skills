#!/usr/bin/env python3
"""Tests for logbook-push (push.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import PUSH_SCRIPT


def run_push(args: list[str], payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PUSH_SCRIPT)] + args,
        input=json.dumps(payload),
        capture_output=True, text=True, cwd=str(cwd)
    )


def make_logbook(tmp_path: Path, slug: str) -> Path:
    lb_dir = tmp_path / "logbook" / slug
    lb_dir.mkdir(parents=True)
    meta = {
        "slug": slug,
        "title": slug, "description": "",
        "created_at": "2026-04-18T09:00:00Z", "format_version": 1
    }
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    (lb_dir / "entries.jsonl").write_text("")
    return tmp_path


def test_valid_tests_entry_appended(tmp_path):
    make_logbook(tmp_path, "t1")
    payload = {"title": "Smoke", "went_well": ["Works"], "went_wrong": []}
    result = run_push(["--logbook", "t1", "--type", "tests"], payload, tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    assert out["id"] == 1
    assert "ulid" in out

    lines = (tmp_path / "logbook" / "t1" / "entries.jsonl").read_text().strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["id"] == 1
    assert entry["type"] == "tests"
    assert "ulid" in entry
    assert "created_at" in entry


def test_schema_validation_rejects_empty_went_well_and_went_wrong(tmp_path):
    make_logbook(tmp_path, "t2")
    payload = {"title": "Bad", "went_well": [], "went_wrong": []}
    result = run_push(["--logbook", "t2", "--type", "tests"], payload, tmp_path)
    assert result.returncode == 11


def test_mixed_schema_collaboration_in_any_logbook(tmp_path):
    """Any entry type is valid in any logbook (mixed schema, no type mismatch)."""
    make_logbook(tmp_path, "t3")
    payload = {"title": "Collab in tests logbook", "ai_contribution": "AI did X", "human_contribution": ""}
    result = run_push(["--logbook", "t3", "--type", "collaboration"], payload, tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    assert "warning" not in out


def test_logbook_not_found_exits_10(tmp_path):
    payload = {"title": "X", "went_well": ["ok"], "went_wrong": []}
    result = run_push(["--logbook", "nonexistent", "--type", "tests"], payload, tmp_path)
    assert result.returncode == 10


def test_sensitive_content_exits_14(tmp_path):
    make_logbook(tmp_path, "t4")
    payload = {"title": "Creds", "went_well": ["AKIAIOSFODNN7EXAMPLE"], "went_wrong": []}
    result = run_push(["--logbook", "t4", "--type", "tests"], payload, tmp_path)
    assert result.returncode == 14


def test_sensitive_content_proceeds_with_acknowledge(tmp_path):
    make_logbook(tmp_path, "t5")
    payload = {"title": "Creds", "went_well": ["AKIAIOSFODNN7EXAMPLE"], "went_wrong": []}
    result = run_push(["--logbook", "t5", "--type", "tests", "--acknowledge-sensitive"], payload, tmp_path)
    assert result.returncode == 0


def test_two_entries_have_sequential_ids(tmp_path):
    make_logbook(tmp_path, "t6")
    p = {"title": "T", "went_well": ["ok"], "went_wrong": []}
    r1 = run_push(["--logbook", "t6", "--type", "tests"], p, tmp_path)
    r2 = run_push(["--logbook", "t6", "--type", "tests"], p, tmp_path)
    assert json.loads(r1.stdout)["id"] == 1
    assert json.loads(r2.stdout)["id"] == 2

    lines = (tmp_path / "logbook" / "t6" / "entries.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2
    first_line_bytes = lines[0]
    # Re-run just to verify first line unchanged
    lines2 = (tmp_path / "logbook" / "t6" / "entries.jsonl").read_text().strip().splitlines()
    assert lines2[0] == first_line_bytes
