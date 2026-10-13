"""Run the assets/starter project end to end in a temporary copy (opt-in, ~30 s).

    KEDRO_RUN_TESTS=1 KEDRO_TEST_PYTHON=/path/to/venv/bin/python python3 -m unittest tests.test_starter -v

The interpreter needs kedro~=1.7, kedro-datasets (pandas csv/parquet, json), pydantic>=2, pytest.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
STARTER = SKILL / "assets" / "starter"
PY = os.environ.get("KEDRO_TEST_PYTHON", "python3")
ENABLED = os.environ.get("KEDRO_RUN_TESTS") == "1"


@unittest.skipUnless(ENABLED, "set KEDRO_RUN_TESTS=1 (and KEDRO_TEST_PYTHON) to run the starter")
class StarterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="kedro-starter-"))
        cls.root = cls.tmp / "starter"
        shutil.copytree(STARTER, cls.root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def kedro(self, *args: str) -> subprocess.CompletedProcess:
        env = {**os.environ, "KEDRO_DISABLE_TELEMETRY": "1", "COLUMNS": "200", "PYTHONDONTWRITEBYTECODE": "1"}
        return subprocess.run([PY, "-m", "kedro", *args], cwd=self.root, capture_output=True, text=True, env=env)

    def test_1_full_run_writes_both_stations(self):
        result = self.kedro("run")
        self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])
        a = json.loads((self.root / "data/08_reporting/station_a_qc_summary.json").read_text())
        b = json.loads((self.root / "data/08_reporting/station_b_qc_summary.json").read_text())
        self.assertEqual((a["rows"], b["rows"]), (2, 2))

    def test_2_soft_merge_keeps_sibling_params(self):
        # min_quality=4 keeps only quality-4 rows; max_wave_height (sibling) must survive the override
        result = self.kedro("run", "--namespaces", "station_a", "--params", "station_a.qc.min_quality=4")
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])
        a = json.loads((self.root / "data/08_reporting/station_a_qc_summary.json").read_text())
        self.assertEqual(a["rows"], 1)  # 19.0 m still filtered -> max_wave_height kept

    def test_3_invalid_param_fails_before_any_node(self):
        result = self.kedro("run", "--params", "station_b.qc.min_quality=9")
        self.assertNotEqual(result.returncode, 0)
        out = result.stdout + result.stderr
        self.assertIn("ParameterValidationError", out)
        self.assertNotIn("Running node", out)

    def test_4_project_tests_pass(self):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=self.root,
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stdout[-2000:])

    def test_6_hook_templates_register_and_enforce(self):
        pkg = self.root / "src" / "obs_qc"
        for name in ("node_timing_hook.py", "data_validation_hook.py"):
            shutil.copy(SKILL / "assets" / "hooks" / name, pkg / name)
        settings = pkg / "settings.py"
        original = settings.read_text()
        try:
            settings.write_text(original + (
                "\nfrom obs_qc.data_validation_hook import DataValidationHook\n"
                "from obs_qc.node_timing_hook import NodeTimingHook\n"
                "HOOKS = (NodeTimingHook(), DataValidationHook("
                "required_columns={'station_a.clean_obs': {'time', 'wave_height'}}))\n"))
            ok = self.kedro("run")
            self.assertEqual(ok.returncode, 0, ok.stderr[-2000:])
            self.assertIn("took", ok.stdout + ok.stderr)
            settings.write_text(settings.read_text().replace("'wave_height'}", "'salinity'}"))
            bad = self.kedro("run")
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("missing required columns: ['salinity']", bad.stdout + bad.stderr)
        finally:
            settings.write_text(original)

    def test_5_snapshot_has_no_findings(self):
        result = subprocess.run([PY, str(SKILL / "scripts" / "kedro_snapshot.py"), "--project", str(self.root)],
                                capture_output=True, text=True, env={**os.environ, "KEDRO_DISABLE_TELEMETRY": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("findings: none", result.stdout)


if __name__ == "__main__":
    unittest.main()
