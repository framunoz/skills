# Notebooks and IPython

Kedro has one interactive mechanism: the IPython extension `kedro.ipython`. Every entry point
(`kedro ipython`, `kedro jupyter lab/notebook`, `%load_ext`) loads that extension. It puts four
project variables into the namespace and registers line magics. All of this was verified on
1.7.0 unless marked otherwise.

## Entry points

| How | What it does | Notes |
|---|---|---|
| `uv run kedro ipython` | Runs `ipython --ext kedro.ipython <extra args>` | Calls `ipython` from `PATH`, so use `uv run`. Extra args pass through: `kedro ipython -c "print(catalog.keys())"` runs non-interactively |
| `uv run kedro jupyter lab` | Creates kernel `kedro_<package>` ("Kedro (<package>)"), then runs `python -m jupyter lab --MultiKernelManager.default_kernel_name=kedro_<package>` | Extra args and `--help` go to Jupyter |
| `uv run kedro jupyter notebook` | Same, with the classic Notebook | Needs `notebook` installed |
| `uv run kedro jupyter setup` | Only creates/replaces the kernel spec in the user Jupyter dir (macOS: `~/Library/Jupyter/kernels/kedro_<package>`) | **Has no `--help`**: `--help` is forwarded and the kernel is still created |
| `%load_ext kedro.ipython` in any IPython kernel | Finds the project from the cwd and defines the variables | Databricks, Colab, VS Code, plain Jupyter |
| `%reload_kedro <project_root>` | Needed when the kernel's cwd is outside the project; Kedro remembers the path for later `%reload_kedro` calls | |

`--env/-e` on `kedro ipython` and `kedro jupyter *` sets `KEDRO_ENV` for the kernel.

Outside a project, `%load_ext kedro.ipython` registers the magics but defines no variables, and
logs:
`Kedro extension was registered but couldn't find a Kedro project. Make sure you run '%reload_kedro <project_root>'.`

## Injected variables

Logged as `Defined global variable 'context', 'session', 'catalog' and 'pipelines'`.

| Name | Type (1.7.0) | Use |
|---|---|---|
| `catalog` | `DataCatalog` (a subclass with catalog-command mixins) | `catalog.load("companies")`, `catalog.save(...)`, `catalog.keys()`, `catalog.filter(name_regex=..., type_regex=..., by_type=...)` |
| `context` | `KedroContext` | `context.params`, `context.env`, `context.project_path`, `context.config_loader` |
| `pipelines` | `_ProjectPipelines` (dict-like) | `pipelines["__default__"]`, `sorted(pipelines)` → registered names |
| `session` | `KedroSession` | `session.run(...)`: **one run per session** |

Line magics after loading: `%reload_kedro`, `%load_node`, and `%run_viz` (registered by the
kedro-viz plugin through the `kedro.line_magic` entry point).

`context.env` is `None` when you did not pass an env, even though the config loader is still
merging `conf/local` (`default_run_env: local` in `settings.py`). Do not use `context.env` to
detect "local" (verified on 1.7.0).

## `%reload_kedro`

Rebuilds all four variables in place, with no kernel restart. Run it after you edit
`catalog.yml` or parameters. Python modules that are already imported are not re-imported by
`%reload_kedro` (standard Python behaviour). For edited node code, use `%autoreload` or restart
the kernel (not tested here).

```
%reload_kedro                                   # same project, fresh session
%reload_kedro /path/to/project                  # set/change project root
%reload_kedro --env=prod                        # or -e prod
%reload_kedro --params "model_options.test_size=0.3,label=a b"
%reload_kedro --conf-source=/path/conf.tar.gz   # also accepts a conf directory
```

`--params` uses the `kedro run --params` syntax: comma-separated `key=value`, with dotted keys
for nested values. Nested values are deep-merged into `parameters.yml`, not replaced. Quoted
values with spaces work (fixed in 1.5.0). Verified: `--env=local --params=model_options.test_size=0.3`
→ `context.params["model_options"]["test_size"] == 0.3`, `context.env == "local"`.

## `%load_node <node_name>`

Generates code that reproduces a node: a `catalog.load(...)` line per input, the imports of the
node's module, the function source (since 1.4 this also pulls in same-module helper
functions, through AST extraction, and warns when it falls back to the function alone), and a
call. In Jupyter/IPython/VS Code it puts the code in the next cell. Elsewhere it prints the code.
The feature is experimental: it emits a `UserWarning` and needs `ipylab>=1.0.0` and
`notebook>=7.0.0` for Jupyter Notebook.

Verified output for the spaceflights `split_data_node`:

```python
# Prepare necessary inputs for debugging
# All debugging inputs must be defined in your project catalog
data = catalog.load("model_input_table")
parameters = catalog.load("params:model_options")
import logging
import pandas as pd
...
def split_data(data: pd.DataFrame, parameters: dict) -> tuple:
    ...
split_data(data, parameters)
```

Requirements and failure modes (verified):

- Pass the **node name**, not the function name. Unknown name →
  `ValueError: Node with name='no_such_node' not found in any pipelines. Remember to specify the node name, not the node function.`
- The inputs must be **persisted** catalog entries. `%load_node train_model_node` still
  generates `X_train = catalog.load("X_train")`, but `X_train` is an in-memory intermediate,
  so that cell fails with `DatasetNotFoundError: Dataset 'X_train' not found in the catalog`.
  Either register the intermediates in `catalog.yml` or run the upstream nodes first.

The debug loop: `%load_node <failing node>` → run the cells → `%debug` (post-mortem) or `%pdb on`.

## Running pipelines from a notebook

```python
session.run()                                   # __default__, like `kedro run`
session.run(pipeline_name="data_processing")    # or pipeline_names=[...]
session.run(node_names=[...], tags=[...], from_nodes=[...], to_outputs=[...],
            namespaces=[...], load_versions={...}, runner=SequentialRunner(),
            only_missing_outputs=True)
```

- The return value is a dict `{dataset_name: dataset_object}` for the pipeline's free outputs.
  It holds dataset objects, not data, so call `.load()`. Persisted outputs live in the catalog
  instead: `catalog.load("model_input_table")`.
- A second `session.run()` raises `KedroSessionError: A run has already been completed as part
  of the active KedroSession. KedroSession has a 1-1 mapping with runs, and thus only one run
  should be executed per session.` → `%reload_kedro` before each run.
- On 1.7.0, `session.run()` with no `runner=` passes `runner='None'` to hooks, so kedro-viz
  logs `Workflow tracking is disabled for non-sequential runners...` and skips
  `.viz/kedro_pipeline_events.json`. To keep workflow tracking, pass
  `runner=SequentialRunner()` (verified; the fix is in an unreleased version).

## Without a project: config loader + catalog only

To use the catalog in a notebook that has no project, without the extension (docs only):

```python
from kedro.config import OmegaConfigLoader
from kedro.io import DataCatalog

conf_loader = OmegaConfigLoader(conf_source=".")
catalog = DataCatalog.from_config(conf_loader["catalog"])
params = conf_loader["parameters"]
```

## Converting a whole notebook: agree on the structure first

For anything bigger than a few cells, propose the decomposition before writing code: node
boundaries, which values become parameters vs constants, and which reads/writes become catalog
entries (with layer) ripple through `nodes.py`, `pipeline.py`, `catalog.yml` and
`parameters*.yml` at once — a wrong split means rewriting all four. Fill
`assets/notebook-sow-template.md` (a short Statement of Work) and wait for the user's OK. If the
user already approved one, or the run is non-interactive, put the SOW at the top of the answer
and continue, listing the assumptions made. A request to "just write the code" is still not an
approval of a structure the user hasn't seen — keep the SOW short instead of skipping it.

Analysis for the SOW:

- **I/O** — every `pd.read_*`, `open`, `.to_csv`, `pickle.dump`, `savefig`, hard-coded path →
  a catalog entry; the dataset type comes from `scripts/check_dataset.py`.
- **Parameters vs constants** — tunable values go to parameters, schema facts stay in code
  (matrix in `cheatsheet.md`).
- **Dependencies** — imports → project deps and `kedro-datasets[...]` extras.
- **Display-only cells** (`df.head()`, `plt.show()`) are dropped, not turned into nodes.

## Moving notebook code into a project

1. Hard-coded paths → entries in `conf/base/catalog.yml`. Read them with `catalog.load("name")`
   in the notebook from the start.
2. Magic numbers → `conf/base/parameters*.yml`, read through `context.params[...]`.
3. Cells → pure functions `def f(inputs...) -> outputs` that do no I/O and never touch
   `catalog` or `context`. Move them into `src/<pkg>/pipelines/<name>/nodes.py`.
4. Wire them into `pipeline.py` with `Node(func, inputs=[...], outputs=..., name="..._node")`,
   with `params:<key>` for parameters. Give every node a name, because `%load_node`, `--nodes`
   and orchestrators all need it.
5. `kedro run --pipelines=<name>`. Then keep the notebook only for exploration: load the outputs
   with `catalog.load` and debug with `%load_node`.

## Gotchas

- **Variables undefined after `%load_ext`** → wrong cwd, or a config/import error. → Run
  `%reload_kedro <root>`, which shows the real error. A broken `catalog.yml` or a failing import
  in `pipeline_registry` blocks all four variables.
- **First `%load_ext` takes ~10 s or more** (about 10 s for spaceflights here) → it imports every pipeline module (sklearn and other
  heavy dependencies) to build `pipelines` and validate typed params. That is normal and not a
  hang. Heavy top-level imports in `nodes.py` make it slower.
- **`kedro ipython` → `FileNotFoundError: [Errno 2] No such file or directory: 'ipython'`** →
  you called the venv's `kedro` without the venv on `PATH`. → `uv run kedro ipython`. Verified on
  1.7.0.
- **Edited `catalog.yml` but `catalog` is stale** → the variables are snapshots. → `%reload_kedro`.
