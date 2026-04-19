#!/usr/bin/env python3
"""Tests for logbook-init (init.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import INIT_SCRIPT


def run_init(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(INIT_SCRIPT)] + args,
        capture_output=True, text=True, cwd=str(cwd)
    )


def test_valid_slug_creates_meta_and_entries(tmp_path):
    result = run_init(["--logbook", "my-tests", "--type", "tests"], tmp_path)
    assert result.returncode == 0
    out = json.loads(result.stdout)
    assert out["ok"] is True
    assert out["logbook"] == "my-tests"
    assert out["schema_type"] == "tests"

    meta_path = tmp_path / "logbook" / "my-tests" / "meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text())
    assert meta["slug"] == "my-tests"
    assert meta["schema_type"] == "tests"
    assert meta["format_version"] == 1
    assert "created_at" in meta

    entries_path = tmp_path / "logbook" / "my-tests" / "entries.jsonl"
    assert entries_path.exists()
    assert entries_path.read_text() == ""


def test_invalid_slug_uppercase_exits_16(tmp_path):
    result = run_init(["--logbook", "MyTests", "--type", "tests"], tmp_path)
    assert result.returncode == 16


def test_invalid_slug_spaces_exits_16(tmp_path):
    result = run_init(["--logbook", "my tests", "--type", "tests"], tmp_path)
    assert result.returncode == 16


def test_duplicate_logbook_exits_17(tmp_path):
    run_init(["--logbook", "dup-log", "--type", "tests"], tmp_path)
    result = run_init(["--logbook", "dup-log", "--type", "tests"], tmp_path)
    assert result.returncode == 17


def test_invalid_type_exits_18(tmp_path):
    result = run_init(["--logbook", "bad-type", "--type", "unknown"], tmp_path)
    assert result.returncode == 18


def test_schema_type_matches_argument(tmp_path):
    run_init(["--logbook", "collab-log", "--type", "collaboration"], tmp_path)
    meta = json.loads((tmp_path / "logbook" / "collab-log" / "meta.json").read_text())
    assert meta["schema_type"] == "collaboration"


def test_format_version_is_1(tmp_path):
    run_init(["--logbook", "free-log", "--type", "free"], tmp_path)
    meta = json.loads((tmp_path / "logbook" / "free-log" / "meta.json").read_text())
    assert meta["format_version"] == 1


def test_title_and_description_optional(tmp_path):
    result = run_init([
        "--logbook", "titled",
        "--type", "tests",
        "--title", "My Title",
        "--description", "A description"
    ], tmp_path)
    assert result.returncode == 0
    meta = json.loads((tmp_path / "logbook" / "titled" / "meta.json").read_text())
    assert meta["title"] == "My Title"
    assert meta["description"] == "A description"
