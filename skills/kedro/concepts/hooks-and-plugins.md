# Hooks and plugins

Hooks let you add behaviour at fixed points of a run without touching nodes. Plugins are
pip-installable packages that add hooks, CLI commands, line magics or starters through entry
points. Both are built on pluggy. Verified on 1.7.0 unless marked otherwise.

## Hook specs (from `kedro.framework.hooks.specs`, 1.7.0)

| Spec | Arguments you may declare | Typical use |
|---|---|---|
| `after_context_created` | `context` | Inject credentials into `context.config_loader["credentials"]`; capture `context.env` for later hooks |
| `after_catalog_created` | `catalog, conf_catalog, conf_creds, parameters, save_version, load_versions` | Inspect/patch datasets, read `dataset.metadata` |
| `before_pipeline_run` | `run_params, pipeline, catalog` | Start an MLflow run, log params, sanity checks |
| `after_pipeline_run` | `run_params, run_result, pipeline, catalog` | Close the tracking run, notify |
| `on_pipeline_error` | `error, run_params, pipeline, catalog` | Alerting, cleanup |
| `before_node_run` | `node, catalog, inputs, is_async, run_id` | Timing start, input checks. **May return `dict[name → value]` to override inputs** |
| `after_node_run` | `node, catalog, inputs, outputs, is_async, run_id` | Timing end, output checks, metric logging |
| `on_node_error` | `error, node, catalog, inputs, is_async, run_id` | `pdb.post_mortem`, alerting |
| `before_dataset_loaded` | `dataset_name, node` | Load timing |
| `after_dataset_loaded` | `dataset_name, data, node` | Load timing, validation |
| `before_dataset_saved` | `dataset_name, data, node` | Validation before write |
| `after_dataset_saved` | `dataset_name, data, node` | Lineage, stats |
| CLI: `before_command_run` | `project_metadata, command_args` | (`kedro.framework.cli.hooks`, `@cli_hook_impl`) |
| CLI: `after_command_run` | `project_metadata, command_args, exit_code` | kedro-telemetry uses these |

The `run_params` keys are `run_id, project_path, env, kedro_version, tags, from_nodes, to_nodes,
node_names, from_inputs, to_outputs, load_versions, runtime_params, pipeline_names, namespaces,
runner, only_missing_outputs`.

On 1.7.0, `run_params["runner"]` is the runner's `repr` under `kedro run`
(`'<kedro.runner.sequential_runner.SequentialRunner object at 0x...>'`) and the string `'None'`
when `session.run()` is called with no runner. Match on a substring, not on equality. The
upcoming release changes this to the runner name.

## Implement and register

```python
# src/<pkg>/hooks.py
import logging, time
from kedro.framework.hooks import hook_impl

log = logging.getLogger(__name__)

class TimingHooks:
    def __init__(self):
        self._t = {}                      # one instance per session → state persists across calls

    @hook_impl
    def before_node_run(self, node):      # declare only the args you need (pluggy opt-in)
        self._t[node.name] = time.perf_counter()

    @hook_impl
    def after_node_run(self, node):
        log.info("%s took %.3fs", node.name, time.perf_counter() - self._t.pop(node.name))
```

```python
# src/<pkg>/settings.py
from <pkg>.hooks import TimingHooks
HOOKS = (TimingHooks(),)                  # instances, not classes
```

Verified rules:

| You do | Result |
|---|---|
| Declare a subset of the spec's args | Works, because pluggy passes only what you declare |
| Give an arg a default (`run_params: dict = {}`) | **Silently receives the default** (`{}`), not Kedro's value |
| Declare an arg the spec lacks (`nodes`) | Run aborts with `PluginValidationError: Plugin '...' for hook 'before_node_run'` / `hookimpl definition: before_node_run(nodes) -> None` / `Argument(s) {'nodes'} are declared in the hookimpl but can not be found in the hookspec` |
| Misspell the method (`before_node_runs`) | **Silently never called**, no error |
| Forget `@hook_impl` | **Silently never called** |
| `HOOKS = (TimingHooks,)` | `TypeError: KedroSession expects hooks to be registered as instances. Have you forgotten the `()` when registering a hook class ?` |

## Execution order

- Order is LIFO within `HOOKS`: with `HOOKS = (A(), B())`, B's implementation runs before A's
  (verified).
- Plugin hooks (auto-discovered through the `kedro.hooks` entry point) are registered *after*
  the project's `HOOKS`, so under LIFO they run *before* them (docs only). The docs also say
  that the overall order "is not guaranteed".
- For a hard guarantee, use `@hook_impl(tryfirst=True)` or `@hook_impl(trylast=True)`, which
  are standard pluggy options.
- To disable a plugin's auto-registered hooks, set `DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)`
  in `settings.py`. Use the **distribution name exactly as its metadata spells it** — Kedro compares
  without normalising: kedro-mlflow must be written `"kedro_mlflow"` (`"kedro-mlflow"` silently does
  nothing; verified with kedro-mlflow 2.0.3). Check with
  `uv run python -c "from importlib.metadata import entry_points; print([e.dist.name for e in entry_points(group='kedro.hooks')])"`.
  Verified: with kedro-viz disabled,
  `.viz/stats.json` and `.viz/kedro_pipeline_events.json` are no longer written.

## Runners and hooks

| Runner | Context/catalog/pipeline hooks | Node and dataset hooks |
|---|---|---|
| `SequentialRunner` (default) | Yes | Yes |
| `ThreadRunner` | Yes | Yes (your hook state must be thread-safe) |
| `ParallelRunner` | Yes (main process) | **No.** Workers don't run them (verified: no `after_node_run` output) |

A project that relies on node or dataset hooks (timing, MLflow per-node logging, validation)
must not use `ParallelRunner`.

## Common recipes

- **Credentials from a secret manager**: in `after_context_created`, run
  `context.config_loader["credentials"] = {**context.config_loader["credentials"], **fetched}`.
  Catalog entries then reference them through `credentials: <key>`.
- **Retry flaky nodes**: in `before_node_run(node)`, run `node.func = retry(node.func)` when
  `"flaky" in node.tags`.
- **Data checks**: `after_dataset_loaded` / `before_dataset_saved`. For schema checks, prefer
  the 1.6+ catalog `validator:` (Pandera), which needs no hook.
- **Experiment tracking**: start the run in `before_pipeline_run`, log `run_params` and params,
  log metrics in `after_node_run`, end the run in `after_pipeline_run` / `on_pipeline_error`.
  kedro-mlflow already implements all of this as a plugin.
- **Debugging**: in `on_node_error`, call `pdb.post_mortem(sys.exc_info()[2])`.
- **Hooks under kedro-viz**: `kedro viz run/build` skip project hooks unless you pass
  `--include-hooks` (verified). This matters when credentials come from
  `after_context_created`.

## Plugins: entry-point groups (`kedro.framework.cli.utils.ENTRY_POINT_GROUPS`)

| Group | Points to | Effect |
|---|---|---|
| `kedro.project_commands` | a `click.Group` | Commands available inside a project |
| `kedro.global_commands` | a `click.Group` | Commands available everywhere (kedro-viz uses this) |
| `kedro.hooks` | a hook **instance** | Auto-registered for every project in the env |
| `kedro.cli_hooks` | a CLI-hook instance (`@cli_hook_impl`) | Runs around every CLI command |
| `kedro.line_magic` | a function | Registered as an IPython line magic by `kedro.ipython` (`%run_viz`) |
| `kedro.init` | a no-arg function (declare `**kwargs`) | Runs before Kedro starts |
| `kedro.starters` | starter specs | Registers project starters for `kedro new` (not tested) |

A minimal CLI plugin (verified; it can live inside the project package itself):

```python
# src/<pkg>/cli_plugin.py
import click

@click.group(name="demo")
def commands(): pass

@commands.command(name="hello")
@click.pass_obj                      # ProjectMetadata
def hello(metadata):
    click.echo(f"HELLO from {metadata.package_name} at {metadata.project_path}")
```

```toml
[project.entry-points."kedro.project_commands"]
demo = "<pkg>.cli_plugin:commands"
```

Then `uv sync` (entry points are read from installed metadata, so reinstall is required), then
`uv run kedro hello`. The group is **merged into the root CLI**: the command is `kedro hello`,
not `kedro demo hello`. For the `kedro <plugin> <cmd>` shape, nest a group inside the group.
Outside a project, project commands are absent: `Error: No such command 'hello'.`
`kedro info` lists installed plugins and their entry-point kinds.

## Notable plugins (PyPI, checked 2026-10-09)

| Package | Latest | Released | Purpose | Kedro 1.x? |
|---|---|---|---|---|
| kedro-viz | 12.5.0 | 2026-09-29 | Pipeline visualisation (`kedro viz`) | Yes |
| kedro-datasets | 9.6.0 | 2026-08-07 | Dataset implementations | `kedro>=1.0.0rc1,<2` |
| kedro-telemetry | 0.9.0 | 2026-09-03 | Anonymous usage stats (Kedro dependency) | Yes |
| kedro-mlflow | 2.0.3 | 2026-05-10 | MLflow tracking, model registry, serving | `kedro>=1.0.0,<2` |
| kedro-airflow | 0.11.0 | 2026-07-15 | `kedro airflow create [--group-by namespace]` → DAG | `kedro>=1.0.0rc1,<2` |
| kedro-docker | 0.6.2 | 2024-11-27 | Dockerfile/image for a project | Pins only `kedro>=0.16`, last release pre-1.0 |
| kedro-databricks | 0.18.3 | 2026-09-01 | Databricks asset bundles | `kedro>=0.19.7` |
| kedro-dagster | 0.8.1 | 2026-10-02 | Translate a project to Dagster | (community, listed in docs) |
| kedro-kubeflow | 0.11.0 | 2026-05-29 | Kubeflow Pipelines | `kedro>0.18.4,<2` |
| kedro-vertexai | 1.0.0 | 2025-08-26 | Vertex AI Pipelines | `kedro>=1.0.0,<2` |
| kedro-azureml | 1.0.0 | 2025-08-24 | Azure ML Pipelines | `kedro>=1.0.0,<2` |
| kedro-sagemaker | 0.4.0 | 2025-02-19 | SageMaker Pipelines | `kedro>=0.19.0`; 1.x support unverified |
| kedro-skills | 0.2.0 | 2026-09-03 | `kedro skills install` agent skills | `kedro>=1.0` |

There is no `kedro-prefect` package on PyPI. Prefect is covered by a docs guide only. The
community list is at github.com/kedro-org/awesome-kedro.
