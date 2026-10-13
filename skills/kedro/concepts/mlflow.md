# MLflow: experiment tracking and model registry

Two paths; prefer **A** unless the plugin can't be added. Never run both on the same run — the
plugin's auto-registered hook already opens and closes the MLflow run.

Verified on kedro 1.7.0 + **kedro-mlflow 2.0.3 + mlflow 3.17.1** (2026-10-13).

| kedro-mlflow | Kedro | MLflow |
|---|---|---|
| 2.x (2.0.0 released 2025-11-25) | `>=1.0,<2` | **3.x** (dropped 2.x) |
| 1.x (1.0.0 released 2025-07-27) | `>=1.0` | 1.x / 2.x |
| 0.12–0.13 | 0.19 | 1.x / 2.x |

## A. `kedro-mlflow` plugin (declarative)

```bash
uv add kedro-mlflow                 # pulls mlflow 3.x
uv run kedro mlflow init            # writes conf/local/mlflow.yml (--env <env>, --force)
```

The plugin's hook registers itself through entry points — **don't** add it to `settings.HOOKS`
(unless `DISABLE_HOOKS_FOR_PLUGINS` disables it).

### Tracking URI: use a database (MLflow ≥ 3.x)

`kedro mlflow init` leaves `mlflow_tracking_uri: null`, which falls back to the file store
`./mlruns`. Recent MLflow refuses it and **the run fails**: `MlflowException: The filesystem
tracking backend (e.g., './mlruns') is in maintenance mode…` (verified on mlflow 3.17.1). Set:

```yaml
# conf/local/mlflow.yml  (only the keys you change)
server:
  mlflow_tracking_uri: sqlite:///mlflow.db     # or http://host:5000 for a shared server
tracking:
  experiment:
    name: obs_qc                                # defaults to the package name
```

Artifacts still go to `./mlruns/` next to the database; git-ignore `mlflow.db` and `mlruns/`.
`MLFLOW_ALLOW_FILE_STORE=true` restores the old file store if you must. For a shared server,
commit `mlflow.yml` in `conf/base` (or `kedro mlflow init --env <env>`); secrets for the server
go in `credentials.yml` and are referenced by `server.credentials: <key>`.

### What gets logged automatically

- **Parameters**: every top-level parameter key of the run (`station_a.qc`, …) (verified).
- Everything declared with a kedro-mlflow dataset, when the node saves it.

### Catalog datasets (nodes stay pure)

| `type:` | Does |
|---|---|
| `kedro_mlflow.io.artifacts.MlflowArtifactDataset` | Wraps any dataset; the saved file is also logged as an artifact (`artifact_path:` optional) |
| `kedro_mlflow.io.metrics.MlflowMetricsHistoryDataset` | Node returns `{"r2": {"value": 0.9, "step": 0}, …}`; logged as `<dataset>.<metric>` (e.g. `wave_metrics.r2`) |
| `kedro_mlflow.io.metrics.MlflowMetricDataset` / `MlflowMetricHistoryDataset` | One metric / one metric's history |
| `kedro_mlflow.io.models.MlflowModelTrackingDataset` | Logs the model with a flavor (`flavor: mlflow.sklearn`); MLflow 3 "logged model" named by `save_args.name` (was `artifact_path`) |
| `kedro_mlflow.io.models.MlflowModelRegistryDataset` | **Loads** a registered model by `alias` **or** `stage_or_version` (both → `DatasetError: You cannot specify 'alias' and 'stage_or_version' simultaneously`). Without `flavor` it returns a `PyFuncModel`; set `flavor: mlflow.sklearn` for the native object |

Working entries: `assets/mlflow/catalog_mlflow.yml` (all verified in a run).

### CLI

| Command | Use |
|---|---|
| `kedro mlflow init` | Create `mlflow.yml` |
| `kedro mlflow ui` | MLflow UI with `ui.host`/`ui.port` from `mlflow.yml` |
| `kedro mlflow modelify` | Export a pipeline as an MLflow model (check `--help` for the current signature) |

Exclude pipelines from tracking with `tracking.disable_tracking.pipelines: [name]`.

## Registry lifecycle (both paths)

1. **Register** a logged model: `mlflow.register_model(model_uri, "wave_model")` (or
   `registered_model_name=` when logging). Creates a version.
2. **Promote** with an alias: `MlflowClient().set_registered_model_alias("wave_model", "champion", version)`.
   Aliases replace the deprecated stages (MLflow ≥ 2.9); prefer them.
3. **Consume**: catalog `MlflowModelRegistryDataset` with `alias: champion`, or
   `mlflow.<flavor>.load_model("models:/wave_model@champion")`.

The catalog dataset only loads; register and alias through the MLflow client (a small script or
an `after_pipeline_run` hook). (all verified)

## B. Native MLflow in hooks (imperative)

Use when the plugin isn't an option. One run per pipeline:
`before_pipeline_run` → `mlflow.start_run()` + `log_params`; `after_node_run` → `log_metrics`
for metric outputs; `after_pipeline_run` → log/register the model, `end_run()`;
`on_pipeline_error` → `end_run(status="FAILED")`. Template: `assets/hooks/mlflow_native_hook.py`
(adapt names; verify against the installed MLflow). Hook mechanics: `concepts/hooks-and-plugins.md`.

## More detail

`integrations-and-plugins/mlflow`; kedro-mlflow docs <https://kedro-mlflow.readthedocs.io/>
and CHANGELOG <https://github.com/Galileo-Galilei/kedro-mlflow/blob/master/CHANGELOG.md>;
MLflow registry <https://mlflow.org/docs/latest/ml/model-registry/>.
