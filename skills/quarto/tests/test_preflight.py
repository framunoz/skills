"""Unit tests for scripts/quarto_preflight.py (stdlib only, no Quarto needed)."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL / "tests" / "fixtures"
SPEC = importlib.util.spec_from_file_location("quarto_preflight", SKILL / "scripts" / "quarto_preflight.py")
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


def stub(directory: Path, version: str) -> Path:
    exe = directory / "quarto"
    exe.write_text(f"#!/bin/sh\necho {version}\n", encoding="utf-8")
    exe.chmod(0o755)
    return exe


def run(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with patch.object(sys, "argv", ["quarto_preflight.py", *argv]), redirect_stdout(out):
        status = preflight.main()
    return status, out.getvalue()


class VersionTests(unittest.TestCase):
    def test_compare(self):
        self.assertEqual(preflight.compare_versions(preflight.SKILL_QUARTO_VERSION), "same as skill")
        self.assertTrue(preflight.compare_versions("1.11.0").startswith("NEWER"))
        self.assertTrue(preflight.compare_versions("1.7.31").startswith("OLDER"))
        self.assertTrue(preflight.compare_versions("garbage").startswith("unknown"))

    def test_minor_versions_compare_numerically(self):
        self.assertTrue(preflight.compare_versions("1.9.0", "1.10.0").startswith("OLDER"))

    def test_reports_version_from_stub(self):
        with tempfile.TemporaryDirectory() as tmp:
            status, out = run("--quarto", str(stub(Path(tmp), "1.11.2")))
        self.assertEqual(status, 0)
        self.assertIn("quarto version: 1.11.2", out)
        self.assertIn("NEWER", out)

    def test_missing_quarto(self):
        status, out = run("--quarto", "definitely-not-quarto-xyz")
        self.assertEqual(status, 1)
        self.assertIn("not found", out)


class ProjectTests(unittest.TestCase):
    def test_profiles_and_metadata(self):
        lines = "\n".join(preflight.inspect_project(FIXTURES / "configuration" / "reports" / "summary.qmd"))
        self.assertIn(f"project root: {(FIXTURES / 'configuration').resolve()}", lines)
        self.assertIn("profiles: _quarto-review.yml", lines)
        self.assertIn("directory metadata: reports/_metadata.yml", lines)
        self.assertIn("documents: 1", lines)

    def test_project_type_default_and_explicit(self):
        self.assertEqual(preflight.project_type(FIXTURES / "configuration" / "_quarto.yml"), "default")
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "_quarto.yml"
            cfg.write_text("project:\n  output-dir: _site\n  type: website\n", encoding="utf-8")
            self.assertEqual(preflight.project_type(cfg), "website")

    def test_no_project_warns_about_rprofile(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = "\n".join(preflight.inspect_project(Path(tmp)))
        self.assertIn("project: none", lines)
        self.assertIn(".Rprofile", lines)

    def test_environment_markers_found_in_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".venv").mkdir()
            (root / "renv.lock").write_text("{}", encoding="utf-8")
            sub = root / "site"
            sub.mkdir()
            (sub / "_quarto.yml").write_text("project:\n  type: website\n", encoding="utf-8")
            lines = "\n".join(preflight.inspect_project(sub))
        self.assertIn("python env:", lines)
        self.assertIn("uv run quarto", lines)
        self.assertIn("r env:", lines)


if __name__ == "__main__":
    unittest.main()
