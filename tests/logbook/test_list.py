#!/usr/bin/env python3
"""Tests for logbook-list (list.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import LIST_SCRIPT


def run_list(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LIST_SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd)
    )


def make_logbook(tmp_path: Path, slug: str, schema_type: str, entries: list[dict] | None = None) -> None:
    lb_dir = tmp_path / "logbook" / slug
    lb_dir.mkdir(parents=True)
    meta = {
        "slug": slug, "schema_type": schema_type,
        "title": slug, "description": "",
        "created_at": "2026-04-18T09:00:00Z", "format_version": 1
    }
    (lb_dir / "meta.json").write_text(json.dumps(meta))
    content = ""
    if entries:
        content = "\n".join(json.dumps(e) for e in entries) + "\n"
    (lb_dir / "entries.jsonl").write_text(content)


def test_empty_logbook_dir_returns_empty_list(tmp_path):
    (tmp_path / "logbook").mkdir()
    result = run_list(["--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    assert out["logbooks"] == []


def test_two_logbooks_listed_correctly(tmp_path):
    e1 = {"id": 1, "ulid": "A1", "created_at": "2026-04-18T10:00:00Z",
          "type": "tests", "title": "T1", "went_well": ["ok"], "went_wrong": []}
    e2 = {"id": 1, "ulid": "B1", "created_at": "2026-04-17T09:15:00Z",
          "type": "collaboration", "title": "C1",
          "ai_contribution": "AI did X", "human_contribution": ""}
    make_logbook(tmp_path, "lb-tests", "tests", [e1])
    make_logbook(tmp_path, "lb-collab", "collaboration", [e2])

    result = run_list(["--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    slugs = {lb["slug"] for lb in out["logbooks"]}
    assert "lb-tests" in slugs
    assert "lb-collab" in slugs

    lb_tests = next(lb for lb in out["logbooks"] if lb["slug"] == "lb-tests")
    assert lb_tests["schema_type"] == "tests"
    assert lb_tests["entries"] == 1
    assert lb_tests["last_entry_at"] == "2026-04-18T10:00:00Z"


def test_directory_without_meta_json_skipped(tmp_path):
    (tmp_path / "logbook" / "not-a-logbook").mkdir(parents=True)
    make_logbook(tmp_path, "real-lb", "free")
    result = run_list(["--project-root", str(tmp_path)], tmp_path)
    out = json.loads(result.stdout)
    slugs = [lb["slug"] for lb in out["logbooks"]]
    assert "not-a-logbook" not in slugs
    assert "real-lb" in slugs


def test_no_logbook_dir_returns_empty_list(tmp_path):
    result = run_list(["--project-root", str(tmp_path)], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["logbooks"] == []
