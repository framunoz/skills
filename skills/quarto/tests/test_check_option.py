"""Integration tests for scripts/check_option.py against the installed Quarto schemas."""

from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("quarto") and shutil.which("uv"), "needs quarto and uv")
class CheckOptionTests(unittest.TestCase):
    def check(self, *names: str) -> tuple[int, str]:
        result = subprocess.run(
            ["uv", "run", "--quiet", str(SKILL / "scripts" / "check_option.py"), *names],
            capture_output=True, text=True, cwd=SKILL,
        )
        return result.returncode, result.stdout

    def test_known_option_reports_formats(self):
        status, out = self.check("code-fold")
        self.assertEqual(status, 0)
        self.assertIn("formats:", out)

    def test_deprecated_option_is_flagged_hidden(self):
        _, out = self.check("highlight-style")
        self.assertIn("hidden:", out)

    def test_project_option_reported_as_nested(self):
        _, out = self.check("execute-dir")
        self.assertIn("nested property", out)
        self.assertIn("project.yml", out)

    def test_unknown_option_suggests_and_fails(self):
        status, out = self.check("code-folding")
        self.assertEqual(status, 1)
        self.assertIn("Did you mean: code-fold", out)


if __name__ == "__main__":
    unittest.main()
