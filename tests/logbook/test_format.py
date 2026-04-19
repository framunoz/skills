#!/usr/bin/env python3
"""Tests for logbook-format (format.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import FORMAT_SCRIPT


def run_format(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(FORMAT_SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd)
    )


def make_logbook(tmp_path: Path, slug: str, entries: list[dict]) -> Path:
    lb_dir = tmp_path / "logbook" / slug
    lb_dir.mkdir(parents=True)
    meta = {
        "slug": slug,
        "title": slug, "description": "",
        "created_at": "2026-04-18T09:00:00Z", "format_version": 1
    }
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    (lb_dir / "entries.jsonl").write_text(
        "\n".join(json.dumps(e) for e in entries) + ("\n" if entries else "")
    )
    return tmp_path


def test_all_entries_rendered(tmp_path):
    entries = [
        {"id": 1, "ulid": "A1", "created_at": "2026-04-18T10:00:00Z",
         "type": "tests", "title": "T1", "went_well": ["ok"], "went_wrong": []},
        {"id": 2, "ulid": "A2", "created_at": "2026-04-18T11:00:00Z",
         "type": "tests", "title": "T2", "went_well": [], "went_wrong": ["bad"]},
    ]
    make_logbook(tmp_path, "fmt1", entries)
    result = run_format(["--logbook", "fmt1"], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    assert out["entries_rendered"] == 2

    rendered = (tmp_path / "logbook" / "fmt1" / "rendered.md").read_text()
    assert "T1" in rendered
    assert "T2" in rendered


def test_empty_optional_fields_render_no_observations(tmp_path):
    entries = [
        {"id": 1, "ulid": "A1", "created_at": "2026-04-18T10:00:00Z",
         "type": "tests", "title": "T1", "went_well": ["ok"], "went_wrong": []},
    ]
    make_logbook(tmp_path, "fmt2", entries)
    run_format(["--logbook", "fmt2"], tmp_path)
    rendered = (tmp_path / "logbook" / "fmt2" / "rendered.md").read_text()
    assert "*No observations*" in rendered


def test_format_twice_produces_identical_output(tmp_path):
    entries = [
        {"id": 1, "ulid": "A1", "created_at": "2026-04-18T10:00:00Z",
         "type": "tests", "title": "T1", "went_well": ["ok"], "went_wrong": []},
    ]
    make_logbook(tmp_path, "fmt3", entries)
    run_format(["--logbook", "fmt3"], tmp_path)
    first = (tmp_path / "logbook" / "fmt3" / "rendered.md").read_bytes()
    run_format(["--logbook", "fmt3"], tmp_path)
    second = (tmp_path / "logbook" / "fmt3" / "rendered.md").read_bytes()
    assert first == second


def test_corrupt_jsonl_line_skipped_script_exits_0(tmp_path):
    lb_dir = tmp_path / "logbook" / "fmt4"
    lb_dir.mkdir(parents=True)
    meta = {"slug": "fmt4", "title": "fmt4",
            "description": "", "created_at": "2026-04-18T09:00:00Z", "format_version": 1}
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    good = {"id": 1, "ulid": "A1", "created_at": "2026-04-18T10:00:00Z",
            "type": "tests", "title": "T1", "went_well": ["ok"], "went_wrong": []}
    (lb_dir / "entries.jsonl").write_text(json.dumps(good) + "\nNOT_JSON\n")
    result = run_format(["--logbook", "fmt4"], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["entries_rendered"] >= 1


def test_entries_sorted_newest_first(tmp_path):
    entries = [
        {"id": 1, "ulid": "A1", "created_at": "2026-04-18T08:00:00Z",
         "type": "tests", "title": "Older", "went_well": ["ok"], "went_wrong": []},
        {"id": 2, "ulid": "A2", "created_at": "2026-04-18T12:00:00Z",
         "type": "tests", "title": "Newer", "went_well": ["ok"], "went_wrong": []},
    ]
    make_logbook(tmp_path, "fmt5", entries)
    run_format(["--logbook", "fmt5"], tmp_path)
    rendered = (tmp_path / "logbook" / "fmt5" / "rendered.md").read_text()
    assert rendered.index("Newer") < rendered.index("Older")
