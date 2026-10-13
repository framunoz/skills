# Running: `kedro run`, runners, sessions, server, inspection, logging

Kedro 1.7.0. "(verified on 1.7.0)" = run in a scratch spaceflights project; the rest comes from
the docs (`build/run_a_pipeline`, `extend/session`, `extend/serving`, `inspect/inspect-project`,
`develop/logging`).

## `kedro run` options (from `kedro run --help`, 1.7.0)

| Option | Notes |
|---|---|
| `--pipelines a,b` | Registered pipelines to run (1.2+). Default `__default__`. Imports only `pipelines/a/`, `pipelines/b/` (1.5+, see the registry trap in `pipelines.md`). |
| `-p, --pipeline NAME` | **Deprecated**: `KedroDeprecationWarning: Option '--pipeline' is deprecated ... Please use '--pipelines' instead.` (verified on 1.7.0) |
| `-e, --env ENV` | Config environment, default `local` (on top of `base`). |
| `--params k=v,k2.sub=v` | Runtime parameters; see the syntax section below. |
| `-r, --runner NAME` | `SequentialRunner` (default), `ThreadRunner`, `ParallelRunner`, or a dotted path to a custom `AbstractRunner`. |
| `--runner-params k=v,...` | Runner constructor kwargs (1.6+): `max_workers=4`, `is_async=True`. |
| `--async` | **Deprecated** (1.6): `KedroDeprecationWarning: Option '--async' is deprecated and will be removed in Kedro 2.0. Please use '--runner-params=is_async=True' instead.` (verified on 1.7.0) |
| `-n, --nodes`, `--from-nodes`, `--to-nodes` | Node names, comma-separated. |
| `--from-inputs`, `--to-outputs` | Dataset names. |
| `-t, --tags` | Comma-separated or repeated; **OR** semantics. |
| `-ns, --namespaces` | Namespace plus its children; exact segment match (1.0+). |
| `-lv, --load-versions ds:VERSION` | Pin a versioned dataset for loading. **Colon**, not `=`: `Expected the form of 'load_versions' to be 'dataset_name:YYYY-MM-DDThh.mm.ss.sssZ',found toy_numbers=... instead` (verified on 1.7.0). |
| `--conf-source PATH` | Config directory other than `conf/`. |
| `-c, --config FILE` | YAML file holding run options (below). |
| `--only-missing-outputs` | Skip nodes whose persisted outputs all exist (1.0+, semantics below). |

The flags combine as an intersection (see "Slicing" in `pipelines.md`).

### `--params` syntax (verified on 1.7.0)

- `--params "toy.n=2,report.label=cli"`: items separated by `,`, key and value by `=`. Dotted
  keys address nested params and **merge** into the YAML: other keys such as `toy.scale` survive.
- Values are type-coerced: `123` becomes int, `1e-3` float, `true` bool; anything else is a
  string.
- **No colon separator**, although `--help` advertises "keys - by colon or equals sign":
  `Error: Invalid format of 'params' option: Item 'report.label:x' must contain a key and a value separated by '='.`
- **No commas inside values** (no lists): `report.label=[1,2]` gives
  `Item '2]' must contain a key and a value separated by '='.` Put lists in a YAML env, or use
  `runtime_params` from Python.

### Run config file (`-c/--config`, verified on 1.7.0)

```yaml
# run.yml -> kedro run -c run.yml
run:
  pipelines: toy            # Python argument names: underscores, not dashes
  tags: calc,gen
  runner: ThreadRunner
  runner_params:
    max_workers: 2
  params: "toy.n=2"         # same string syntax as --params
  # node_names, from_nodes, to_nodes, from_inputs, to_outputs, namespaces, env, load_versions, ...
```

Options given on the CLI win over the file: `kedro run -c run.yml --tags gen` ran only the
`gen` node.

### `--only-missing-outputs` semantics (verified on 1.7.0)

Pipeline: `make_numbers → toy_numbers (JSON, persisted) → double → toy_doubled (memory) → total → toy_total (JSON)`.

| State on disk | Nodes run |
|---|---|
| all outputs exist | none: `Skipping all 3 nodes (all persistent outputs exist)` |
| `toy_total` deleted | `double` and `total`: `Skipping 1 nodes with existing outputs: make_numbers`. The memory-output node re-runs because a needed node depends on it. |
| `toy_numbers` deleted (upstream) | **only `make_numbers`**: `Skipping 2 nodes with existing outputs: double, total` |

The check is about **existence, not staleness**. Regenerating an upstream output does not
re-run downstream nodes whose outputs already exist, unlike `make`. After a change upstream,
delete the downstream outputs or use `--from-nodes`.

### Common run errors (verified on 1.7.0)

```text
ValueError: Pipeline does not contain nodes named ['totl'].
ValueError: Pipeline contains no nodes after applying all provided filters. ...   # --tags nope, empty scaffold, or disjoint filters
ValueError: Pipeline input(s) {'toy_doubled'} not found in the DataCatalog...     # slice cut off a MemoryDataset producer
ImportError: An error occurred while importing the 'demo_project.pipelines.toyy' module.   # unknown --pipelines name (raise_errors=True)
TypeError: SequentialRunner.__init__() got an unexpected keyword argument 'max_workers'    # --runner-params without --runner
AttributeError: module 'kedro.runner' has no attribute 'Nope'                              # bad --runner
ParameterValidationError: Parameter validation failed: ...                                  # typed params, before any node runs
```

## Runners

| Runner | Use when | Constraints |
|---|---|---|
| `SequentialRunner` (default) | Most runs; little branching; memory-heavy nodes; debugging | None |
| `ThreadRunner` | I/O-bound nodes (remote reads/writes, DB, API calls); Spark (`SparkDataset` needs threads, not processes); cloud `fsspec` datasets | No async I/O: `UserWarning: 'ThreadRunner' doesn't support loading and saving the node inputs and outputs asynchronously with threads. Setting 'is_async' to False.` (verified on 1.7.0). Datasets must be thread-safe. |
| `ParallelRunner` | CPU-bound pure-Python nodes on independent branches | Multiprocessing: nodes and datasets must pickle; **no `node`/`dataset` hooks**; catalog becomes `SharedMemoryDataCatalog` (the CLI switches it automatically) |

`is_async=True` (Sequential/Parallel) loads and saves the inputs and outputs of each node with
threads, which helps nodes with many I/O datasets.

### ParallelRunner details

- Up-front pickling check (verified on 1.7.0):
  `AttributeError: The following nodes cannot be serialised: [Node(<lambda>, 'a', 'b', 'lam')]`
  followed by "nodes should not include lambda functions, nested functions, closures, etc. If you
  are using custom decorators ensure they are correctly decorated using functools.wraps()". The
  error also occurs with `KEDRO_MP_CONTEXT=fork`.
- `KEDRO_MP_CONTEXT=fork|forkserver|spawn` picks the start method. Any other value silently
  falls back to the system default, as does leaving it unset (source). The defaults are `spawn`
  on macOS and Windows, `fork` on Linux up to Python 3.13, and `forkserver` on Linux with
  Python 3.14+. With `spawn`, everything a node touches must be importable and picklable.
- Cloud-backed datasets (S3/GCS/ADLS through fsspec) often fail to pickle, and 1.6+ warns
  about it in catalog validation. Use `ThreadRunner` for them.
- Observed on macOS (`spawn`): Kedro's own `Running node:` lines appear, but `logger.info(...)`
  calls from the project's node code **did not**. The same run under Sequential/Thread showed
  them (verified on 1.7.0). Don't rely on node INFO logs under ParallelRunner.
- From Python you must pass `SharedMemoryDataCatalog`. A plain `DataCatalog` fails with
  `AttributeError: 'DataCatalog' object has no attribute 'validate_catalog'`. The returned
  `SharedMemoryDataset` objects could **not** be `.load()`ed after `run()` returned
  (`DatasetError`, the manager was already shut down), contrary to the `build/run_a_pipeline`
  example (verified on 1.7.0). Persist the outputs you need, or use the CLI or session.

## Programmatic runs

```python
from pathlib import Path
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.runner import ThreadRunner

root = Path.cwd()                      # the dir containing pyproject.toml
bootstrap_project(root)                # reads pyproject, sys.path, settings.py, registry
with KedroSession.create(project_path=root, env=None,
                         runtime_params={"toy": {"n": 5}}) as session:   # nested dict!
    out = session.run(pipeline_names=["toy"], to_nodes=["double"],
                      runner=ThreadRunner(max_workers=2))
data = {name: ds.load() for name, ds in out.items()}
```

Verified on 1.7.0:

- `session.run(...)` takes the same filters as the CLI: `pipeline_names`, `tags`, `node_names`,
  `from_nodes`, `to_nodes`, `from_inputs`, `to_outputs`, `namespaces`, `load_versions`,
  `only_missing_outputs`, and `runner=` as an **instance**. `pipeline_name=` still works but logs
  "`pipeline_name` is deprecated ... use `pipeline_names`" (source).
- **Return value:** a `dict` keyed by the pipeline's terminal outputs (`pipeline.outputs()`),
  whose values are **dataset objects**, not data. Persisted outputs come back as their catalog
  dataset (e.g. `JSONDataset`), memory outputs as `MemoryDataset`. Call `.load()`. Since 1.0
  every terminal output is returned, whatever the catalog configuration.
- `runtime_params` with **dotted keys does not nest**: `{"toy.n": 3}` was silently ignored
  (`toy.n` stayed 4). Use `{"toy": {"n": 3}}`, which merges with the YAML. This differs from
  CLI `--params toy.n=3`.
- One run per session:
  `KedroSessionError: A run has already been completed as part of the active KedroSession. KedroSession has a 1-1 mapping with runs, and thus only one run should be executed per session.`
- `session.load_context()` gives `context.catalog`, `context.params`, `context.config_loader`.
- Notebooks and IPython: `%load_ext kedro.ipython` / `%reload_kedro` instead of bootstrapping by
  hand.

### `KedroServiceSession` (1.4+, experimental, may change)

A long-lived session for many runs, each with its own `runtime_params` (verified on 1.7.0: two
runs with `n=2` and `n=3` returned totals 3.0 and 9.0):

```python
from kedro.framework.session import KedroServiceSession
s = KedroServiceSession.create(project_path=root)          # also env, conf_source, session_id, serving_mode
out = s.run(pipeline_names=["toy"], runtime_params={"toy": {"n": 2}})
s.close()
```

`create()` takes no `runtime_params` or `save_on_close`; parameters go to `run()`.
`serving_mode=True` preloads every pipeline, which makes concurrent `run()` calls safe.

## HTTP server: `kedro server start` (1.5+)

Requires `kedro[server]` (FastAPI and uvicorn). The server is minimal: no auth, no queue, no
per-request isolation. **Never expose it publicly.**

```bash
kedro server start [-H 127.0.0.1] [-p 8000] [--reload] [-e ENV] [--conf-source PATH]
```

| Endpoint | Behaviour (verified on 1.7.0) |
|---|---|
| `GET /health` | `{"status":"healthy","kedro_version":"1.7.0"}` |
| `GET /snapshot[?params=k=v,...]` | Project snapshot as JSON (same data as `get_project_snapshot`). `params` resolves `${runtime_params:...}` (1.7). |
| `POST /run` | JSON body, every field optional: `pipeline_names`, `params` (a real nested dict), `tags`, `node_names`, `from_nodes`, `to_nodes`, `from_inputs`, `to_outputs`, `namespaces`, `load_versions`, `runner`, `is_async`, `only_missing_outputs`. Returns `{"status":"success","run_id":...,"duration_ms":...}`. |
| `GET /docs` | FastAPI interactive docs (also `/openapi.json`) |

- A run failure still returns JSON with `"status":"failure"` and
  `"error":{"type":"ParameterValidationError","message":...}`. **Check `status`.**
- Unknown body fields are rejected (strict model):
  `{"detail":[{"type":"extra_forbidden","loc":["body","pipeline"],"msg":"Extra inputs are not permitted",...}]}`.
  The field is `pipeline_names`, not `pipeline`.
- `env` and `conf_source` are fixed at startup (`--env`/`KEDRO_SERVER_ENV`,
  `--conf-source`/`KEDRO_SERVER_CONF_SOURCE`) and cannot be set per request.
- At startup it warns that it uses `KedroServiceSession` and ignores `SESSION_CLASS` from
  settings.
- Runner security: dotted runner paths must live in `kedro.runner`, the project package, or
  `RUNNER_MODULE_ALLOWLIST` in `settings.py` (renamed from `RUNNER_MODULES_WHITELIST` in 1.6).
  A catalog `type:` resolved from request `params` is rejected.
- Programmatic: `from kedro.server import create_http_server; app = create_http_server(project_path=...)`.

## Inspecting a project without running it

### CLI

```bash
kedro registry list                 # registered pipeline names (loads all pipelines)
kedro registry describe toy         # default: __default__; lists "- full.node.name (func_name)"
```

### `kedro.inspection.get_project_snapshot` (1.4+; `func_name` and `source` 1.6+; `runtime_params` 1.6+)

`kedro.inspection` exports only `get_project_snapshot` in 1.7.0 (`validate_deployment_grouping`
is in "Upcoming Release" and **does not exist** in 1.7.0). Nothing is executed or loaded.
Verified on 1.7.0:

```python
from pathlib import Path
from kedro.inspection import get_project_snapshot

snap = get_project_snapshot(Path("/path/to/project"))   # also env=, conf_source=, metadata=, runtime_params=
snap.metadata          # ProjectMetadataSnapshot(project_name='Demo Project', package_name='demo_project', kedro_version='1.7.0')
[p.name for p in snap.pipelines]                         # ['__default__', 'toy', ...]
toy = next(p for p in snap.pipelines if p.name == "toy")
toy.inputs, toy.outputs                                  # ['params:report', 'params:toy'], ['toy_total']
for n in toy.nodes:                                      # topological order
    n.name, n.func_name, n.inputs, n.outputs, n.tags, n.namespace
    n.source  # NodeSourceSnapshot(filepath='src/demo_project/pipelines/toy/nodes.py', line_start=19, line_end=21)
snap.datasets["companies"].type, snap.datasets["companies"].filepath   # 'pandas.CSVDataset', 'data/01_raw/companies.csv'
snap.parameters        # TOP-LEVEL keys only: ['a', 'b', 'model_options', 'report', 'toy']
```

- `datasets` contains catalog entries only. Implicit `MemoryDataset`s (`toy_doubled`) are
  absent; entries resolved through factory patterns are included (docs).
- `source` is `None` for lambdas, partials, built-ins, or code outside the project.
- Calling it repeatedly: `metadata = bootstrap_project(root)` once, then
  `get_project_snapshot(metadata=metadata, env="staging")`.
- Typical uses: CI assertions ("pipeline X exists, every node is named, dataset Y is
  configured"), and generating docs or diagrams.

## Logging

- Without `conf/logging.yml` or `KEDRO_LOGGING_CONFIG`, Kedro uses its bundled
  `rich_logging.yml` and logs `Using '.../kedro/framework/project/rich_logging.yml' as logging configuration.`
  (verified on 1.7.0).
- `conf/logging.yml` is **picked up automatically** when present: removing
  `KEDRO_LOGGING_CONFIG` still loaded it (verified on 1.7.0). `KEDRO_LOGGING_CONFIG=/path/x.yml`
  points elsewhere. Changing `CONF_SOURCE` does not move the logging file; set the variable.
- **1.7.0 security change:** custom handler, filter or formatter `class:` entries must come from
  `logging`, `logging.handlers`, `kedro.logging`, or a module listed in
  `KEDRO_LOGGING_MODULE_ALLOWLIST` (comma-separated prefixes). Otherwise every `kedro` command
  fails at startup (verified on 1.7.0):
  `ValueError: Module 'demo_project.logutil' specified as a logging class is not permitted. Only 'logging', 'kedro.logging', and modules listed in the KEDRO_LOGGING_MODULE_ALLOWLIST environment variable are allowed.`
  Fix: `export KEDRO_LOGGING_MODULE_ALLOWLIST=demo_project.logutil`.
- The `()` factory key is not allowed in `logging.yml` (it can execute code); use `class:`.
- In node code, use `logging.getLogger(__name__)`. A project-template `logging.yml` provides
  `rich`, `console` and `info_file_handler` (`info.log`). `DEBUG` level also turns on pluggy hook
  tracing, which is slow and noisy.
