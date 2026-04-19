#!/usr/bin/env python3
"""Tests for amendment entries via push.py and rendering via format.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import FORMAT_SCRIPT, PUSH_SCRIPT


def run_push(args: list[str], payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PUSH_SCRIPT)] + args,
        input=json.dumps(payload),
        capture_output=True, text=True, cwd=str(cwd)
    )


def run_format(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(FORMAT_SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd)
    )


def make_logbook(tmp_path: Path, slug: str, entries: list[dict] | None = None) -> Path:
    lb_dir = tmp_path / "logbook" / slug
    lb_dir.mkdir(parents=True)
    meta = {
        "slug": slug,
        "title": slug, "description": "",
        "created_at": "2026-04-18T09:00:00Z", "format_version": 1
    }
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    if entries:
        (lb_dir / "entries.jsonl").write_text(
            "\n".join(json.dumps(e) for e in entries) + "\n"
        )
    else:
        (lb_dir / "entries.jsonl").write_text("")
    return tmp_path


def test_valid_amendment_appended(tmp_path):
    make_logbook(tmp_path, "amend1")
    # Push original entry
    r1 = run_push(["--logbook", "amend1", "--type", "tests"],
                  {"title": "Original", "went_well": ["Works"], "went_wrong": []}, tmp_path)
    assert r1.returncode == 0
    out1 = json.loads(r1.stdout)
    orig_id = out1["id"]
    orig_ulid = out1["ulid"]

    # Push amendment
    amend_payload = {
        "title": f"Amend #{orig_id}: correction",
        "amends": {"id": orig_id, "ulid": orig_ulid},
        "reason": "Typo correction",
        "body": "The fix only applies to Safari."
    }
    r2 = run_push(["--logbook", "amend1", "--type", "amendment"], amend_payload, tmp_path)
    assert r2.returncode == 0
    out2 = json.loads(r2.stdout)
    assert out2["ok"] is True
    assert out2["id"] == 2

    lines = (tmp_path / "logbook" / "amend1" / "entries.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2


def test_amendment_with_nonexistent_id_exits_13(tmp_path):
    make_logbook(tmp_path, "amend2")
    run_push(["--logbook", "amend2", "--type", "tests"],
             {"title": "Orig", "went_well": ["ok"], "went_wrong": []}, tmp_path)

    amend_payload = {
        "title": "Bad amend",
        "amends": {"id": 999, "ulid": "NONEXISTENT00000000000000"},
        "reason": "Test",
        "body": "body"
    }
    r = run_push(["--logbook", "amend2", "--type", "amendment"], amend_payload, tmp_path)
    assert r.returncode == 13


def test_amendment_with_mismatched_ulid_exits_13(tmp_path):
    make_logbook(tmp_path, "amend3")
    r1 = run_push(["--logbook", "amend3", "--type", "tests"],
                  {"title": "Orig", "went_well": ["ok"], "went_wrong": []}, tmp_path)
    orig_id = json.loads(r1.stdout)["id"]

    amend_payload = {
        "title": "Bad ulid amend",
        "amends": {"id": orig_id, "ulid": "WRONGULID0000000000000000"},
        "reason": "Test",
        "body": "body"
    }
    r = run_push(["--logbook", "amend3", "--type", "amendment"], amend_payload, tmp_path)
    assert r.returncode == 13


def test_format_renders_amendment_backlink(tmp_path):
    make_logbook(tmp_path, "amend4")
    r1 = run_push(["--logbook", "amend4", "--type", "tests"],
                  {"title": "Original entry", "went_well": ["all good"], "went_wrong": []}, tmp_path)
    out1 = json.loads(r1.stdout)

    amend_payload = {
        "title": f"Amend #{out1['id']}: scope",
        "amends": {"id": out1["id"], "ulid": out1["ulid"]},
        "reason": "Clarification",
        "body": "Only affects Safari."
    }
    run_push(["--logbook", "amend4", "--type", "amendment"], amend_payload, tmp_path)
    run_format(["--logbook", "amend4"], tmp_path)

    rendered = (tmp_path / "logbook" / "amend4" / "rendered.md").read_text()
    assert "Amended by #2" in rendered


def test_original_entry_bytes_unchanged_after_amendment(tmp_path):
    make_logbook(tmp_path, "amend5")
    r1 = run_push(["--logbook", "amend5", "--type", "tests"],
                  {"title": "Orig", "went_well": ["ok"], "went_wrong": []}, tmp_path)
    out1 = json.loads(r1.stdout)

    entries_path = tmp_path / "logbook" / "amend5" / "entries.jsonl"
    first_line_before = entries_path.read_text().splitlines()[0]

    amend_payload = {
        "title": "Amend #1",
        "amends": {"id": out1["id"], "ulid": out1["ulid"]},
        "reason": "Fix",
        "body": "Corrected."
    }
    run_push(["--logbook", "amend5", "--type", "amendment"], amend_payload, tmp_path)

    first_line_after = entries_path.read_text().splitlines()[0]
    assert first_line_before == first_line_after
