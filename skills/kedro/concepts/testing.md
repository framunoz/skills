# Testing

Test code, not data. To check data, declare a `validator:` on the catalog entry (1.6+, see the
dataset-validation docs). Use pytest. Everything here was verified on 1.7.0 with the template
created by `kedro new --tools=lint,test,data`.

## What the template gives you

```
tests/
├── __init__.py
├── test_run.py                         # full KedroSession run (an integration smoke test)
└── pipelines/
    ├── __init__.py
    └── data_science/test_pipeline.py   # node unit tests + SequentialRunner pipeline test
```

`pyproject.toml` (with the `test` tool):

```toml
[project.optional-dependencies]
dev = ["pytest-cov>=3,<7", "pytest-mock>=1.7.1, <2.0", "pytest~=7.2", "ruff~=0.12.0"]

[tool.pytest.ini_options]
addopts = "--cov-report term-missing --cov src/<package> -ra"

[tool.coverage.report]
fail_under = 0
show_missing = true
exclude_lines = ["pragma: no cover", "raise NotImplementedError"]
```

Run `uv sync --extra dev`, then `uv run pytest` **from the project root**. Coverage runs on
every pytest call because of `addopts`. Add `--no-cov` for fast iterations, or raise
`fail_under` to enforce a minimum in CI. The docstring in `test_run.py` says tests go in
`src/tests`. That is stale: the template uses `tests/` at the root.

## Three levels

| Level | What | Speed | Touches disk/config |
|---|---|---|---|
| Node unit | Call the function directly | ms | No |
| Pipeline | `SequentialRunner().run(pipeline, DataCatalog of MemoryDatasets)` | ms–s | No |
| Project/session | `bootstrap_project` + `KedroSession.create(...)` | s | Yes: reads `conf/`, runs hooks, writes outputs |

### Node unit test

Nodes are plain functions, so test them with fixtures:

```python
def test_split_data(dummy_data, dummy_parameters):
    X_train, X_test, y_train, y_test = split_data(dummy_data, dummy_parameters["model_options"])
    assert len(X_train) == 2
```

### Pipeline test with in-memory data (verified, passes)

```python
import pandas as pd
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner
from demo_project.pipelines.data_processing import create_pipeline

def test_data_processing_pipeline_in_memory():
    companies = pd.DataFrame({"id": [1, 2], "company_rating": ["90%", "80%"], "iata_approved": ["t", "f"]})
    shuttles = pd.DataFrame({"id": [10, 20], "company_id": [1, 2], "d_check_complete": ["t", "f"],
                             "moon_clearance_complete": ["f", "t"], "price": ["$1,000.0", "$2,000.0"]})
    reviews = pd.DataFrame({"shuttle_id": [10, 20], "review_scores_rating": [90.0, 80.0]})
    catalog = DataCatalog({n: MemoryDataset(d) for n, d in
                           {"companies": companies, "shuttles": shuttles, "reviews": reviews}.items()})
    out = SequentialRunner().run(create_pipeline(), catalog)
    mit = out["model_input_table"].load()          # run() returns datasets, not data
    assert len(mit) == 2 and mit["price"].dtype == float
```

- Missing outputs are created as `MemoryDataset` on the fly. You only provide the inputs, and
  parameters as `"params:<key>"` entries.
- `catalog["x"] = df` (as in the template) also works: raw values get wrapped in a
  `MemoryDataset`.
- `runner.run()` returns `{name: dataset}` for the **free outputs** only, meaning outputs no
  node consumes. Intermediates are not returned. To test one, slice the pipeline with
  `.to_outputs("x")` / `.to_nodes(...)`, or put it in the catalog first and load it afterwards.
- Slice the pipeline to test a sub-chain:
  `create_pipeline().from_nodes("split_data_node").to_nodes("evaluate_model_node")`.
- Unsatisfied inputs raise `ValueError: Pipeline input(s) {...} not found in the DataCatalog`.
- To assert the run succeeded through logs (the template pattern): set
  `caplog.set_level(logging.DEBUG, logger="kedro")`, then check that
  `"Pipeline execution completed successfully"` is in `caplog.text`.

### Project/session test

```python
from pathlib import Path
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

PROJECT = Path(__file__).resolve().parents[N]   # don't rely on Path.cwd()

def test_session_params():
    bootstrap_project(PROJECT)                    # configures settings + pipelines registry
    with KedroSession.create(project_path=PROJECT, env="local",
                             runtime_params={"model_options": {"test_size": 0.5}}) as session:
        params = session.load_context().params
        assert params["model_options"]["test_size"] == 0.5

def test_session_run():
    bootstrap_project(PROJECT)
    with KedroSession.create(project_path=PROJECT) as session:
        out = session.run(pipeline_name="data_processing")   # one run per session
```

- `KedroSession.create(project_path, save_on_close=True, env=None, runtime_params=None, conf_source=None)`.
- `runtime_params` takes a **nested dict**. Dotted keys like `{"model_options.test_size": 0.5}`
  are *not* expanded here (only the CLI `--params` parser expands them); they are silently
  ignored. Nested values are deep-merged: sibling keys from YAML survive (verified).
- The template's `test_run.py` uses `Path.cwd()`. Run from `tests/` and it fails with
  `RuntimeError: Could not find the project configuration file 'pyproject.toml' in .../tests.`
- Session tests use the real `conf/` (base + local), real hooks, and real file datasets. A full
  `session.run()` **writes into `data/`**. Keep them few, or point `conf_source` at a test
  config dir whose catalog writes to `tmp_path`.

## Typed parameters (1.3+)

When a node input is `params:x` and the function hints `x` as a dataclass or a Pydantic v2
model (`uv add "kedro[pydantic]"`), Kedro builds the object from the YAML dict before any node
runs.

| Path | Is the dict converted? | Verified result |
|---|---|---|
| `context.params` / `session.run()` / `kedro run` | Yes | `type(params["typed_options"]) is ModelOptions` |
| `SequentialRunner().run(...)` with a raw dict in the catalog | **No**: the runner does not validate | `AttributeError: 'dict' object has no attribute 'features'` |
| Calling the node function directly | No | Pass the typed object yourself |

So unit and pipeline tests must pass `MemoryDataset(ModelOptions(...))`, not the dict. To test
validation itself, use a session:

```python
with KedroSession.create(project_path=PROJECT,
                         runtime_params={"typed_options": {"bogus": 1}}) as s:
    with pytest.raises(ParameterValidationError):   # kedro.validation.exceptions
        s.load_context().params
```

The message (dataclass):
`Parameter validation failed:\n- Parameter 'typed_options': Failed to instantiate ModelOptions for parameter 'typed_options': ModelOptions.__init__() got an unexpected keyword argument 'bogus'`.

- Dataclasses only check field names and arity. `test_size: "abc"` passes. Use Pydantic for
  value and type constraints.
- **Typing one consumer converts the parameter for all consumers.** If node A hints
  `params:model_options` as `ModelOptions` while node B (`split_data(parameters: dict)`) indexes
  it as a dict, B fails at run time with `TypeError: 'ModelOptions' object is not subscriptable`
  (verified). Type every consumer, or give the typed node its own key.
- Since 1.4, `kedro run --pipelines=<name>` inspects only the selected pipelines' signatures.
  The parameters docs page still says "validates across all pipelines". That part is stale.

## Gotchas

- **The test passes locally but `bootstrap_project` fails in CI** → the cwd is not the project
  root. → Resolve the root from `__file__`, or run `uv run pytest` from the root.
- **Coverage noise / slow runs** → `--cov` is in `addopts`. → `uv run pytest --no-cov -x`
  while iterating.
- **Sessions in several tests** → each test needs its own `KedroSession.create(...)` (one run
  per session). Calling `bootstrap_project` again is harmless.
