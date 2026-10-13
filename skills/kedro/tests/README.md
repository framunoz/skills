# Tests

Run from the skill root. Fast tests need only Python; the rest need an interpreter with
`kedro[pydantic]==1.7.*`, `kedro-datasets` (pandas csv/parquet/excel, json, yaml, pickle,
matplotlib, plotly, api extras), `pytest` and `joblib` — **without kedro-mlflow** (its
auto-registered hook would try to track the starter runs).

```bash
python3 -m unittest discover -s tests                                   # preflight, pointers, fences
KEDRO_TEST_PYTHON=/path/.venv/bin/python python3 -m unittest discover -s tests       # + snapshot, check_dataset, catalog assets
KEDRO_RUN_TESTS=1 KEDRO_TEST_PYTHON=/path/.venv/bin/python python3 -m unittest discover -s tests   # + starter end to end (~10 s)
```

| File | Covers |
|---|---|
| `test_scripts.py` | `kedro_preflight.py` (version compare, stale-pattern and node I/O lint, blocking findings), `kedro_snapshot.py`, `check_dataset.py` |
| `test_catalog_assets.py` | every `assets/catalog/*.yml` entry instantiates; local ones save and load |
| `test_starter.py` | `assets/starter` runs, soft merge, typed-param failure, project tests, snapshot clean, hook templates |
| `test_pointers.py` | file pointers exist, cited doc paths are in `references.md`, balanced code fences |

MLflow material (`concepts/mlflow.md`, `assets/mlflow/`, `assets/hooks/mlflow_native_hook.py`) was
verified manually with kedro-mlflow 2.0.3 / mlflow 3.17.1 on 2026-10-13; re-check on upgrades.
