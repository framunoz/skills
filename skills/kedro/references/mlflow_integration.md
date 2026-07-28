# 📊 MLflow Integration (experiment tracking & model registry)

This reference covers adding **experiment tracking** (params, metrics, artifacts) and a **model registry** (versioning, staging, aliases) to a Kedro 1.0+ project. There are two paths; **prefer Path A** unless you have a specific reason not to.

- **Path A — the `kedro-mlflow` plugin (recommended, idiomatic).** Declarative: tracking is wired through `catalog.yml` datasets and a single `mlflow.yml` config. Hooks register automatically.
- **Path B — native MLflow SDK inside custom Kedro hooks.** Imperative: you call `mlflow.start_run()` / `log_params` / `log_metrics` / `log_artifact` yourself from hook methods. Use only when you need full manual control or can't add the plugin.

> ⚠️ **This ecosystem moves fast.** `kedro-mlflow` reached 1.0.0 (Jul 2025) and 2.0.0 (Nov 2025), and the MLflow 2.x → 3.x boundary changed the model-dataset API (see §1.1 and §3). **Always confirm the exact version pins at install time** — don't assume an example here matches the version you installed.

---

## Path A — the `kedro-mlflow` plugin

### A.1 Version compatibility (read this first)

`kedro-mlflow` is tightly coupled to both Kedro and MLflow major versions. Pick the line that matches your stack:

| Your Kedro | Use `kedro-mlflow` | Requires MLflow |
| :--- | :--- | :--- |
| **1.0+** (this skill's target) | **`>= 1.0.0`** | 1.x / 2.x on the `1.x` line; **3.x** on the `2.x` line |
| 0.19.x | `0.12.x` – `0.13.x` | 1.x / 2.x |

Key facts (verified against the official CHANGELOG and migration guide):
- **`kedro-mlflow 1.0.0`** (released 2025-07-27) is the first release that supports `kedro>=1.0.0` and dropped `kedro==0.19.X`.
- **`kedro-mlflow 2.0.0`** (released 2025-11-25) added MLflow **3.0+** support and **dropped MLflow 2.x**. The current `2.0.x` line pins roughly `kedro>=1.0,<2.0` and `mlflow>=3.0,<4.0`.
- If you are on **MLflow 2.x**, stay on the `kedro-mlflow 1.x` line. If you are on **MLflow 3.x**, use the `2.x` line — and note the model-dataset API change in §3.
- Dataset classes use the **`Dataset`** suffix (lowercase `s`), not the legacy `DataSet`. The rename happened in `kedro-mlflow 0.12.0`, matching Kedro's own `>=0.19` convention. Always write `MlflowArtifactDataset`, never `MlflowArtifactDataSet`.

### A.2 Install & initialize

The plugin attaches to an **existing** Kedro project — there is **no `kedro mlflow new`** command. Create the project first, then init MLflow:

```bash
# 1. (if needed) create the Kedro project
kedro new --name <PROJECT> --tools=data,lint,test --example=no --telemetry=no

# 2. add the plugin (this project uses uv)
uv add kedro-mlflow            # equivalent to: pip install --upgrade kedro-mlflow

# 3. generate conf/local/mlflow.yml
kedro mlflow init              # flags: --env=<env> (default local), --force to overwrite
```

**Hooks auto-register.** On `kedro>=0.16.4`, the plugin's `MlflowHook` is registered automatically via setuptools entry points — **you do not touch `settings.py`**. (Manual `HOOKS = (MlflowHook(),)` wiring is only needed on the ancient 0.16.0–0.16.3 range, or if you've disabled plugin hooks via `DISABLE_HOOKS_FOR_PLUGINS`.) Note the registration comes from the plugin entry point + Kedro version, not from `mlflow.yml` itself — `mlflow.yml` governs *tracking behavior*, not whether the hook loads.

### A.3 The `mlflow.yml` config

`kedro mlflow init` writes `conf/local/mlflow.yml` with three top-level sections. A minimal, working config:

```yaml
server:
  mlflow_tracking_uri: mlruns          # null -> falls back to mlflow.get_tracking_uri(); use a path, or http://host:5000
  mlflow_registry_uri: null            # null -> falls back to the tracking_uri
  credentials: null                    # null -> or a key into credentials.yml

tracking:
  disable_tracking:
    pipelines: []                      # list pipeline names here to exclude them from tracking
  experiment:
    name: <your_python_package>        # defaults to {{ python_package }} via Jinja
    create: true
  run:
    id: null                           # null -> the plugin opens/closes a run automatically
    name: null
    nested: true                       # allow nested runs
  params:
    dict_params:
      flatten: false
    long_params_strategy: fail         # what to do when a param string exceeds MLflow's length limit

ui:
  port: "5000"
  host: "127.0.0.1"
```

A copy-paste version lives at **`assets/mlflow/mlflow.yml`**.

> `conf/local` is the documented default (it's git-ignored, good for personal/dev tracking URIs). For a shared tracking server, put `mlflow.yml` in an environment that is committed (e.g. `conf/base` or a dedicated env via `kedro mlflow init --env=...`).

### A.4 Declarative tracking via the Data Catalog

This is the core idea: instead of logging inside nodes (which violates the pure-function rule — see Core Principle #1), you **wrap or declare datasets in `catalog.yml`** and the plugin logs them to the active run automatically. Your nodes stay pure.

| Dataset (`kedro_mlflow.io...`) | Module | What it does |
| :--- | :--- | :--- |
| `MlflowArtifactDataset` | `.artifacts` | **Wraps any Kedro dataset.** On `save()`, the underlying file (`.csv`, `.png`, `.pkl`, …) is also logged to MLflow as an artifact. |
| `MlflowMetricsHistoryDataset` | `.metrics` | Logs several metrics **with their full history** (step-by-step) to the run. |
| `MlflowMetricDataset` / `MlflowMetricHistoryDataset` | `.metrics` | Singular variants for a single metric / single metric history. |
| `MlflowModelTrackingDataset` | `.models` | **Logs/loads a model by MLflow flavor** (e.g. `mlflow.sklearn`) to/from a run. |
| `MlflowModelRegistryDataset` | `.models` | **Loads a registered model** from the Model Registry by name + stage/version or alias. |

**Artifact (wraps an existing dataset):**
```yaml
prediction_plot:
  type: kedro_mlflow.io.artifacts.MlflowArtifactDataset
  dataset:                                   # the underlying Kedro dataset, declared as usual
    type: matplotlib.MatplotlibWriter
    filepath: data/08_reporting/prediction_plot.png
  # artifact_path: plots                     # optional: subfolder under the run's artifact root
  # run_id: null                             # optional: defaults to the active run
```

**Metrics:**
```yaml
training_metrics:
  type: kedro_mlflow.io.metrics.MlflowMetricsHistoryDataset
  # a node returns e.g. {"rmse": {"value": 0.21, "step": 0}, "mae": {"value": 0.15, "step": 0}}
```

**Model (log to the run by flavor):**
```yaml
trained_model:
  type: kedro_mlflow.io.models.MlflowModelTrackingDataset
  flavor: mlflow.sklearn                     # any importable MLflow flavor module
  save_args:
    name: water_quality_model                # MLflow 3.x / kedro-mlflow 2.x: artifact_path was RENAMED to `name`
```

**Model (load a registered model):**
```yaml
production_model:
  type: kedro_mlflow.io.models.MlflowModelRegistryDataset
  model_name: water_quality_model
  # stage_or_version: production             # a stage ("staging"/"production") or a version number
  alias: champion                            # MLflow 2.9.0+; MUTUALLY EXCLUSIVE with stage_or_version
```

Full, commented snippets are in **`assets/mlflow/catalog_mlflow.yml`**.

### A.5 CLI commands

| Command | Purpose |
| :--- | :--- |
| `kedro mlflow init [--env=<env>] [--force]` | Create `mlflow.yml` (and update the `run.py` template). |
| `kedro mlflow ui` | Launch the MLflow UI using `port`/`host` from `mlflow.yml` (overridable at runtime). |
| `kedro mlflow modelify` | Package a pipeline as a standalone MLflow model (advanced; check current docs for the signature). |

---

## Path B — native MLflow SDK inside Kedro hooks

When you can't use the plugin, drive MLflow yourself from a hook class (see `references/hooks_architecture.md` for the lifecycle and the pluggy gotchas). The canonical pattern from the official Kedro docs scopes a **single run** across the pipeline lifecycle:

- `before_pipeline_run` → `mlflow.start_run(...)` + `mlflow.log_params(run_params)`
- `after_node_run` → `mlflow.log_metrics(...)` for any metric outputs
- `after_pipeline_run` → `mlflow.<flavor>.log_model(...)` and end the run
- `on_pipeline_error` → end the run cleanly so a failure doesn't leave a dangling active run

A ready-to-adapt example is in **`assets/hooks/mlflow_native_hook.py`**. Register it in `settings.py`:
```python
from <my_project>.hooks import MlflowNativeHook
HOOKS = (MlflowNativeHook(),)
```

> ⚠️ **Don't run both paths at once on the same run.** If `kedro-mlflow` is installed its auto-registered hook already manages the run lifecycle; a second hand-rolled `start_run` will fight it. Pick one path.

---

## Model registry lifecycle (applies to both paths)

The registry sits *on top of* tracking. Typical lifecycle:

1. **Register** a logged model — either at log time with `mlflow.<flavor>.log_model(..., registered_model_name="water_quality_model")`, or after the fact with `mlflow.register_model(model_uri, name)`. This creates a new **version**.
2. **Promote** — assign an **alias** (e.g. `champion`, `challenger`) to a version via `MlflowClient().set_registered_model_alias(name, alias, version)`.
3. **Consume** — load by alias/version. With `kedro-mlflow`, use `MlflowModelRegistryDataset` (§A.4); natively, `mlflow.<flavor>.load_model("models:/water_quality_model@champion")`.

> **Stages vs aliases:** older MLflow used named *stages* (`Staging`, `Production`). MLflow **2.9.0+** introduced **aliases** as the recommended mechanism and deprecated stages; MLflow 3.x leans fully on aliases + tags. `MlflowModelRegistryDataset` accepts `alias` **or** `stage_or_version`, never both. Prefer aliases on new projects.

> **MLflow 3.x semantics:** a logged model is **no longer necessarily tied to a run**. That's why `kedro-mlflow 2.x` dropped `run_id` from `MlflowModelTrackingDataset` and renamed `artifact_path` → `name`. Keep this in mind when migrating older catalogs.

---

## ⚠️ Caveats & things NOT verified

These came out of the research with low confidence — **do not present them as settled; check current docs before using:**

- **`pipeline_ml_factory`** (declaratively packaging a train+inference pipeline as one logged MLflow model) was **refuted** in verification — the API name/signature did not survive cross-checking. If a user wants single-artifact pipeline packaging, point them to the current `kedro-mlflow` docs rather than reproducing an unverified signature.
- The **native-hook code (Path B)** is the *documented pattern* from `docs.kedro.org`, but a full, version-pinned working example for **MLflow 3.x** was not independently verified. Treat `assets/hooks/mlflow_native_hook.py` as a starting template to validate against the installed versions.
- **Writing to the registry from the catalog**: `MlflowModelRegistryDataset` is documented as the **load** side. For programmatic registration/aliasing, use the native MLflow client (`mlflow.register_model` / `MlflowClient`).

---

## 🔗 Authoritative sources

- **kedro-mlflow repo & docs**: https://github.com/Galileo-Galilei/kedro-mlflow · https://kedro-mlflow.readthedocs.io/
- **Datasets API**: https://kedro-mlflow.readthedocs.io/en/stable/source/05_API/01_python_objects/01_Datasets.html
- **CHANGELOG (version pins)**: https://github.com/Galileo-Galilei/kedro-mlflow/blob/master/CHANGELOG.md
- **Kedro's MLflow integration page**: https://docs.kedro.org/en/stable/integrations-and-plugins/mlflow/
- **Native hooks example**: https://docs.kedro.org/en/latest/hooks/examples.html
- **MLflow Model Registry**: https://mlflow.org/docs/latest/ml/model-registry/
