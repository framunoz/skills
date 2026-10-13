"""Tests for the skill's scripts.

Preflight tests are stdlib-only. Snapshot/dataset tests need an interpreter with Kedro 1.7 and
kedro-datasets: they use KEDRO_TEST_PYTHON (path to a project venv's python) or the current
interpreter, and skip when neither can import Kedro.
    python3 -m unittest discover -s tests
    KEDRO_TEST_PYTHON=/path/to/project/.venv/bin/python python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL / "tests" / "fixtures"
PY = os.environ.get("KEDRO_TEST_PYTHON", sys.executable)

spec = importlib.util.spec_from_file_location("kedro_preflight", SKILL / "scripts" / "kedro_preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def has(module: str) -> bool:
    return subprocess.run([PY, "-c", f"import {module}"], capture_output=True).returncode == 0


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "KEDRO_DISABLE_TELEMETRY": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([PY, str(SKILL / "scripts" / script), *args], capture_output=True, text=True, env=env)


class PreflightTests(unittest.TestCase):
    def test_version_compare(self):
        self.assertEqual(preflight.compare(preflight.SKILL_KEDRO_VERSION), "same as skill")
        self.assertTrue(preflight.compare("1.10.0").startswith("NEWER"))   # numeric, not lexical
        self.assertTrue(preflight.compare("0.19.14").startswith("OLDER"))

    def test_tool_kedro_parsing(self):
        meta = preflight.tool_kedro(FIXTURES / "lint-project" / "pyproject.toml")
        self.assertEqual(meta["package_name"], "oldpkg")
        self.assertEqual(meta["kedro_init_version"], "0.19.14")

    def test_lint_finds_every_stale_pattern(self):
        hits = "\n".join(preflight.lint(FIXTURES / "lint-project"))
        for expected in ("kedro.extras.datasets", "DataSet", "OmegaConfigLoader", "layer:", "RUNNER_MODULE_ALLOWLIST", "--pipelines", "--namespaces"):
            self.assertIn(expected, hits)

    def test_node_io_lint(self):
        hits = "\n".join(preflight.node_io(FIXTURES / "lint-project", "src"))
        self.assertIn("etl/nodes.py:5", hits)
        self.assertIn("etl/nodes.py:6", hits)
        self.assertEqual(preflight.node_io(SKILL / "assets" / "starter", "src"), [])

    def test_lint_clean_project_is_quiet(self):
        self.assertEqual(preflight.lint(FIXTURES / "snapshot-project"), [])

    def test_blocking_findings(self):
        lines, blocking = preflight.project_report(FIXTURES / "lint-project", "1.7.0")
        text = "\n".join(lines)
        self.assertTrue(blocking)
        self.assertIn("MAJOR MISMATCH", text)
        self.assertIn("SECRETS IN conf/base", text)


@unittest.skipUnless(has("kedro.inspection"), "needs Kedro >= 1.4 (set KEDRO_TEST_PYTHON)")
class SnapshotTests(unittest.TestCase):
    def test_findings_on_flawed_fixture(self):
        result = run("kedro_snapshot.py", "--project", str(FIXTURES / "snapshot-project"))
        out = result.stdout
        self.assertEqual(result.returncode, 1, result.stderr)  # free-input + param are blocking
        for expected in ("[free-input] __default__: stations", "[param]", "params:thresholds",
                         "[memory] __default__: enriched", "[memory-output] __default__: summary",
                         "[unused] -: never_used", "[auto-name]"):
            self.assertIn(expected, out)
        self.assertNotIn("INFO", out)  # logging is routed away from stdout

    def test_unknown_pipeline(self):
        result = run("kedro_snapshot.py", "--project", str(FIXTURES / "snapshot-project"), "--pipeline", "nope")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not registered", result.stdout + result.stderr)


@unittest.skipUnless(has("kedro_datasets"), "needs kedro-datasets (set KEDRO_TEST_PYTHON)")
class CheckDatasetTests(unittest.TestCase):
    def test_known_type(self):
        out = run("check_dataset.py", "pandas.CSVDataset").stdout
        self.assertIn("extra:    kedro-datasets[pandas-csvdataset]", out)
        self.assertIn("/api/kedro_datasets/pandas.CSVDataset/", out)

    def test_old_casing_and_removed_module(self):
        result = run("check_dataset.py", "pandas.CSVDataSet", "kedro.extras.datasets.pandas.CSVDataSet")
        self.assertEqual(result.returncode, 1)
        self.assertIn("old casing", result.stdout)
        self.assertIn("REMOVED", result.stdout)

    def test_experimental_needs_full_path(self):
        out = run("check_dataset.py", "netcdf.NetCDFDataset").stdout
        self.assertIn("type: kedro_datasets_experimental.netcdf.NetCDFDataset", out)


if __name__ == "__main__":
    unittest.main()
