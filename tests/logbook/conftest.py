#!/usr/bin/env python3
"""Shared pytest fixtures for logbook plugin tests."""
import shutil
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"

PLUGIN_ROOT = Path(__file__).parent.parent.parent / "plugins" / "logbook"
PUSH_SCRIPT = PLUGIN_ROOT / "skills" / "logbook-push" / "scripts" / "push.py"
FORMAT_SCRIPT = PLUGIN_ROOT / "skills" / "logbook-format" / "scripts" / "format.py"
INIT_SCRIPT = PLUGIN_ROOT / "skills" / "logbook-init" / "scripts" / "init.py"
LIST_SCRIPT = PLUGIN_ROOT / "skills" / "logbook-list" / "scripts" / "list.py"
QUERY_SCRIPT = PLUGIN_ROOT / "skills" / "logbook-query" / "scripts" / "query.py"


@pytest.fixture
def tmp_logbook(tmp_path):
    """Factory: set up a temp project dir with a pre-populated logbook.

    Usage: lb_path = tmp_logbook("tests")  → returns project root (tmp_path)
    The logbook is at tmp_path/logbook/fixture-<schema_type>/
    """
    def _make(schema_type: str) -> Path:
        slug = f"fixture-{schema_type}"
        lb_dir = tmp_path / "logbook" / slug
        lb_dir.mkdir(parents=True)

        meta_src = FIXTURES_DIR / f"meta_{schema_type}.json"
        shutil.copy(meta_src, lb_dir / "meta.json")

        entries_src = FIXTURES_DIR / f"entries_{schema_type}.jsonl"
        if entries_src.exists():
            shutil.copy(entries_src, lb_dir / "entries.jsonl")
        else:
            (lb_dir / "entries.jsonl").write_text("")

        return tmp_path

    return _make
