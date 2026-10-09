"""Render fixtures into a temporary copy and check the claims the skill makes about them.

Opt-in (slow, needs quarto; the R fixture needs Rscript with knitr/rmarkdown):
    QUARTO_RENDER_TESTS=1 python3 -m unittest tests.test_render_fixtures -v
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ENABLED = os.environ.get("QUARTO_RENDER_TESTS") == "1" and shutil.which("quarto")


@unittest.skipUnless(ENABLED, "set QUARTO_RENDER_TESTS=1 (and install quarto) to render fixtures")
class RenderFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="quarto-fixtures-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def render(self, fixture: str, target: str, *args: str) -> tuple[Path, str]:
        root = self.tmp / fixture
        shutil.copytree(FIXTURES / fixture, root)
        result = subprocess.run(["quarto", "render", target, *args], cwd=root, capture_output=True, text=True)
        log = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, log)
        self.assertNotRegex(log, r"WARN(ING)?\b.*(crossref|Unable)", log)
        return root, log

    def test_cross_references_all_resolve(self):
        root, _ = self.render("cross-references", "cross-references.qmd", "--to", "html")
        html = (root / "cross-references.html").read_text(encoding="utf-8")
        self.assertNotIn("?@", re.sub(r"<script.*?</script>", "", html, flags=re.S))
        for label in ("fig-panels", "fig-first", "tbl-results", "eq-energy", "box-summary", "lst-greeting", "sec-overview"):
            self.assertIn(f'href="#{label}"', html, label)

    def test_revealjs_fragments_and_vertical(self):
        root, _ = self.render("revealjs", "revealjs.qmd")
        html = (root / "revealjs.html").read_text(encoding="utf-8")
        self.assertNotIn("{.fragment}", html)
        self.assertIn('class="fragment"', html)
        self.assertIn("incremental", html)
        # Quarto's `vertical` is emitted as reveal's `default` (up/down within stacks)
        self.assertIn("navigationMode: 'default'", html)
        self.assertEqual(html.count("<section>\n<section"), 2)

    @unittest.skipUnless(shutil.which("Rscript"), "needs Rscript with knitr")
    def test_execute_dir_under_project_runs_from_root(self):
        root, _ = self.render("profile-freeze-execute-dir", "reports/report.qmd")
        md = (root / "reports" / "report.md").read_text(encoding="utf-8")
        self.assertIn("cwd: profile-freeze-execute-dir", md)

    def test_one_source_three_formats(self):
        root, _ = self.render("formats", "formats.qmd")
        for ext in ("html", "docx", "pdf"):
            self.assertTrue((root / f"formats.{ext}").exists(), ext)

    def test_citations_resolve(self):
        root, log = self.render("citations", "citations.qmd", "--to", "html")
        self.assertNotIn("Citeproc: citation", log)
        self.assertIn("Knuth", (root / "citations.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
