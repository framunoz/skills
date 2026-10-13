---
name: kedro
description: Kedro data-pipeline projects — creating projects, nodes and pipelines (namespaces, registry, slicing), the Data Catalog and kedro-datasets (factories, versioning, partitions, credentials, validation), configuration with OmegaConfigLoader (environments, parameters, --params, runtime_params, globals, typed parameters), runners and `kedro run`, hooks and plugins, MLflow tracking (kedro-mlflow), notebooks, testing, Kedro-Viz, packaging/deployment, migrating 0.19 projects to 1.x, and productionizing a notebook or analysis script into Kedro nodes, pipelines and catalog datasets. Use whenever the user works in a repo with `[tool.kedro]` in pyproject.toml, edits `conf/**/catalog*.yml` or `parameters*.yml`, writes nodes/pipelines/hooks, or hits a `kedro` CLI error — even if they don't say "Kedro". Not for isolated generic terms (node, pipeline, parameter, dataset) without Kedro context, orchestration tools (Airflow, Prefect, Dagster, dbt) on their own, or plain pandas code.
license: MIT
compatibility: Kedro 1.x (written and tested on 1.7.0) with kedro-datasets; scripts need the project's Python env (uv recommended).
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 3.0.0
  kedro-version: 1.7.0
  kedro-datasets-version: 9.6.0
  kedro-mlflow-version: 2.0.3
  created: 2026-10-09
  last-reviewed: 2026-10-13
  source: https://github.com/framunoz/skills
  inspiration: book-to-skill progressive disclosure; Kedro MCP / kedro-skills guidance
  tags: data-science, pipelines, kedro, reproducibility
---

# Kedro

Distilled, version-checked notes for building and debugging Kedro projects. Concepts in
`concepts/`; traps in `gotchas.md`; proven patterns in `recipes.md`; decision tables in
`cheatsheet.md`; terms in `glossary.md`; official docs per topic in `references.md`; a runnable
example project in `assets/starter/`; templates in `assets/` (catalog, hooks, MLflow, SOW).
Paths are relative to this skill's directory; `<skill>` below means that directory.

## 1. Preflight — do this first

Run with the **project's** interpreter (the shell's `python` usually isn't it):

```bash
uv run python <skill>/scripts/kedro_preflight.py
```

It prints the interpreter (and whether it is a virtualenv), versions of kedro / kedro-datasets /
kedro-viz / omegaconf / pydantic, the comparison with **Kedro 1.7.0 + kedro-datasets 9.6.0**
(written and tested 2026-10-09), project metadata, `conf/` environments and files, settings
in use, and a lint of pre-1.x patterns (`kedro.extras`, `DataSet`, `ConfigLoader`, top-level
`layer:`, `--namespace`, `--pipeline`, removed `DataCatalog` methods, secrets in `conf/base`,
direct I/O such as `.to_csv(`/`pd.read_*` inside node modules).

- **Same version** — trust this skill's API and option names.
- **Newer** — read the `RELEASE.md` entries in between
  (`https://raw.githubusercontent.com/kedro-org/kedro/main/RELEASE.md`) before relying on an
  API here; verify signatures with `inspect.signature` / `--help` in the project env.
- **Older** — say so; features tagged with a version here (e.g. 1.6 dataset validation, 1.4
  inspection API) may be missing.
- **Kedro not importable** — the wrong interpreter; find the project env (`.venv`, `uv run`)
  before concluding anything. Never report versions from the base interpreter.

## 2. Operating rules

- **Inspect before editing**: `uv run python <skill>/scripts/kedro_snapshot.py` shows pipelines,
  node inputs/outputs, declared datasets and parameters, and flags undeclared/unpersisted
  datasets, missing params and unnamed nodes — without running anything. Follow the project's
  conventions (layers, naming, file split) and make the smallest change that works.
- **Run to verify**: `uv run kedro run --pipelines <name>` (or a narrower slice) and
  `uv run pytest`. Say beforehand that a run **writes outputs** under `data/` (overwriting
  non-versioned files) and may read/write cloud storage; prefer the smallest pipeline/slice.
- **Confirm first** — state the exact command and get an explicit yes for: writing to remote or
  production storage (`--env prod`, `s3://…` outputs), deleting `data/` contents or versions,
  editing credentials, `kedro package`/deployment, installing a plugin that registers hooks or
  CLI commands, and `kedro jupyter setup` (installs a user-level kernel). Adding a
  `kedro-datasets` extra the task needs is normal — mention it.
- **Secrets never go in `conf/base/`** — only `conf/<env>/credentials.yml`, referenced by key.

## 3. Mental model

```
conf/base ─┬─ conf/local (or --env X) ─┬─ --params / runtime_params
           └──────── OmegaConfigLoader ┘        │
                 catalog config   parameters ───┘
                       │               │ params:x
                       ▼               ▼
  KedroSession → KedroContext → DataCatalog ──load──▶ Node(pure function) ──save──▶ DataCatalog
                                     ▲                 (Pipeline = DAG of named nodes,
  pipeline_registry.find_pipelines ──┘                  composed, namespaced, sliced)
  Runner (Sequential | Thread | Parallel) drives it; hooks fire around every step.
  Name not in the catalog → MemoryDataset: exists only during the run.
```

| Symptom | Layer | Probe |
|---|---|---|
| Value not what you set; credentials not found; interpolation error | Config | `concepts/configuration.md`; `ctx.params` in `kedro ipython`; check which env loaded |
| Dataset error, wrong type, file not written | Catalog | `check_dataset.py`; `kedro catalog resolve-patterns`; snapshot `memory` findings |
| Node not found, wrong nodes ran, input "not found in the DataCatalog" | Pipeline | snapshot; `kedro registry describe <name>`; node names |
| Fails only with some runner / in deployment | Runner/packaging | `concepts/running.md`, `concepts/deployment-and-viz.md` |
| Unexpected side effect, timing, tracking | Hooks | `concepts/hooks-and-plugins.md` |

## 4. Writing rules

- **Nodes are pure functions**: data and params in, data out; no catalog/IO/Kedro imports
  inside. This keeps them testable without Kedro.
- **Name every node** (`name=`): default names are `func__<hash>` and change when inputs change.
- **Type-hint node functions**; scaffold new pipelines with `uv run kedro pipeline create <name>`
  (it also creates `parameters_<name>.yml` and tests, and `--pipelines` only finds pipelines in
  their own `pipelines/<name>/` folder). `Node`/`Pipeline` and `node()`/`pipeline()` are both
  valid in 1.x — follow the project's style; only `kedro.pipeline.modular_pipeline` is gone.
- **Declare every dataset that must outlive the run**; everything else is memory.
- **Verify dataset types** with `uv run python <skill>/scripts/check_dataset.py <type>` before
  writing an entry: it confirms the type exists in the installed kedro-datasets, lists the
  constructor args, the extra to `uv add`, and the docs URL. Experimental types need the full
  `kedro_datasets_experimental.…` path.
- **Parameters through `params:`** (`params:model_options`, `params:model_options.lr`); type them
  with a Pydantic v2 model for validation. Prefer `merge_strategy: {parameters: soft}` so
  overrides touch single keys.
- **Current CLI**: `--pipelines` (not `--pipeline`), `--namespaces` (not `--namespace`),
  `kedro catalog describe-datasets|list-patterns|resolve-patterns`.
- **Layers in metadata**: `metadata: {kedro-viz: {layer: raw}}`, never a top-level `layer:`.
- **Everything through uv**: `uv run kedro …`, `uv add "kedro-datasets[<extra>]"`;
  `pyproject.toml` is the dependency source of truth.

## 5. Where to look

Read only the files the task touches.

| Task | Read |
|---|---|
| New project, layout, `settings.py`, dependencies with uv, starters | `concepts/project.md` |
| `conf/` envs, parameters, `--params`, `runtime_params`, globals, credentials, typed params | `concepts/configuration.md` |
| Catalog entries, dataset types, factories, transcoding, versioning, partitions, validation, `DataCatalog` API | `concepts/catalog.md` |
| Nodes, pipelines, namespaces/reuse, registry, slicing | `concepts/pipelines.md` |
| `kedro run` flags, runners, sessions from Python, HTTP server, inspection, logging | `concepts/running.md` |
| Jupyter/IPython, `%reload_kedro`, `%load_node` | `concepts/notebooks.md` |
| Convert a notebook / script into a pipeline | `concepts/notebooks.md` → "Converting a whole notebook" (SOW first: `assets/notebook-sow-template.md`) |
| Unit/pipeline/project tests | `concepts/testing.md` |
| Hooks, CLI plugins, notable plugins (airflow, databricks…) | `concepts/hooks-and-plugins.md`; templates in `assets/hooks/` |
| Experiment tracking, model registry (kedro-mlflow or native MLflow) | `concepts/mlflow.md`; `assets/mlflow/`, `assets/hooks/mlflow_native_hook.py` |
| Packaging, orchestrator grouping, platform guides, Kedro-Viz, telemetry | `concepts/deployment-and-viz.md` |
| Something fails or behaves oddly | `gotchas.md` first, then the topic file |
| "How do I…" | `recipes.md` |
| Choosing dataset type, runner, merge strategy, where config goes | `cheatsheet.md` |
| A working reference project | `assets/starter/` (namespaced reuse, factories, typed params, tests; run-tested on 1.7.0) |
| Catalog entry examples per dataset type | `assets/catalog/*.yml` (instantiated by tests; local ones saved and loaded) |

**Beyond this skill**: `references.md` maps topics to the official docs, each available as
Markdown at `https://docs.kedro.org/en/stable/<path>/index.md` (index:
`https://docs.kedro.org/en/stable/llms.txt`). Several official pages are wrong for 1.7.0 where
this skill says "(docs say …)" — trust the verified note.

## 6. Report

End with: files changed; pipelines/nodes/datasets added or modified; commands actually run
(env, pipelines, params) and their result including warnings; outputs written and where;
dependencies added; anything assumed or left unverified.
