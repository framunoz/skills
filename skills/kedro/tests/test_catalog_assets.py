"""Every catalog snippet in assets/ parses and instantiates; local ones also save and load.

Needs an interpreter with Kedro + kedro-datasets (KEDRO_TEST_PYTHON). Datasets whose optional
dependencies are missing there are reported as skipped, not failed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
PY = os.environ.get("KEDRO_TEST_PYTHON", sys.executable)

PROBE = r"""
import glob, json, os, sys, tempfile, yaml
from kedro.io import DataCatalog
creds = {"model_store": {"key": "k", "secret": "s"}, "my_postgres_db": {"con": "sqlite://"}}
results = {}
files = sorted(glob.glob(sys.argv[1] + "/catalog/*.yml"))
os.chdir(tempfile.mkdtemp())
for f in files:
    for name, entry in (yaml.safe_load(open(f)) or {}).items():
        key = f"{os.path.basename(f)}:{name}"
        try:
            cat = DataCatalog.from_config({name: entry}, credentials=creds); cat[name]
            results[key] = "ok"
        except Exception as e:  # noqa: BLE001
            text = " ".join(str(e).split())
            missing = any(s in text for s in ("No module named", "Install s3fs", "not found in", "Please install"))
            results[key] = "missing-deps" if missing else f"error: {text[:300]}"
        if results[key] == "ok" and name in ("raw_users", "intermediate_users", "model_metrics", "external_business_rules"):
            import pandas as pd
            data = pd.DataFrame({"created_at": ["2026-01-01"], "x": [1]}) if "users" in name else {"a": 1}
            cat.save(name, data); cat.load(name)
            results[key] = "roundtrip"
print(json.dumps(results))
"""


def can_import_kedro() -> bool:
    return subprocess.run([PY, "-c", "import kedro_datasets, yaml"], capture_output=True).returncode == 0


@unittest.skipUnless(can_import_kedro(), "needs kedro-datasets + pyyaml (set KEDRO_TEST_PYTHON)")
class CatalogAssetTests(unittest.TestCase):
    def test_snippets_instantiate(self):
        out = subprocess.run([PY, "-c", PROBE, str(SKILL / "assets")], capture_output=True, text=True,
                             env={**os.environ, "KEDRO_DISABLE_TELEMETRY": "1"})
        self.assertEqual(out.returncode, 0, out.stderr[-2000:])
        results = json.loads(out.stdout.strip().splitlines()[-1])
        self.assertGreaterEqual(len(results), 11)
        errors = {k: v for k, v in results.items() if v.startswith("error")}
        self.assertEqual(errors, {})
        self.assertGreaterEqual(sum(v == "roundtrip" for v in results.values()), 3)


if __name__ == "__main__":
    unittest.main()
