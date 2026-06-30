# Kedro Syntax & Migration Cheat Sheet (legacy → 1.0+)

This is the **read-first** reference. It maps the syntax of **legacy (pre-1.0) Kedro** to **modern Kedro 1.0+**. Use it for two purposes:

- **Authoring / hooking / converting**: to make sure the code you write uses the current 1.0+ API and never reintroduces a deprecated pattern.
- **Migrating**: to upgrade an existing project off any older version onto 1.0+.

The single most common mistake — across *all* Kedro work — is mixing legacy and modern syntax (e.g. a lowercase `node()` next to a capitalized `Pipeline`, or a `CSVDataSet` in a 1.0+ catalog). Calibrate on this list before touching code.

## Core principles of migration

1. **Capitalization matters.** Kedro 1.0+ moved from functional wrappers (`node()`, `pipeline()`) to explicit classes (`Node`, `Pipeline`). Using the wrong case is the #1 cause of failures.
2. **Dataset normalization.** All dataset classes must end in `Dataset`, not `DataSet`.
3. **Namespace pluralization.** The `--namespace` CLI argument is gone; use `--namespaces` instead, even for a single value.
4. **Configuration resolution.** Legacy `ConfigLoader` / `TemplatedConfigLoader` must be replaced by `OmegaConfigLoader`, which supports `${...}` interpolation.

## 1. Pipeline classes (the most frequent error)

- **Legacy:** `from kedro.pipeline.modular_pipeline import node, pipeline`
- **Modern (1.0+):** `from kedro.pipeline import Node, Pipeline`
- **Change:** `node(func=f, inputs="i", outputs="o")` → `Node(func=f, inputs="i", outputs="o")`
- **Change:** `pipeline([nodes], pipe=...)` → `Pipeline(nodes=[nodes])` (note the argument name `nodes`).

## 2. Dataset naming (Dataset vs DataSet)

- **Problem:** Kedro 1.0+ is strict about `Dataset` casing.
- **Fix:** Search and replace `DataSet` with `Dataset` across all `catalog.yml` and Python files.
- **Examples:** `pandas.CSVDataSet` → `pandas.CSVDataset`, `pickle.PickleDataSet` → `pickle.PickleDataset`.

## 3. Catalog & configuration

- `KedroDataCatalog` → `DataCatalog`
- `ConfigLoader` / `TemplatedConfigLoader` → `OmegaConfigLoader`
- Datasets now live in the `kedro-datasets` package (the old `kedro.extras` location was retired). E.g. `pandas.CSVDataset` requires `kedro-datasets[pandas]`.
- `catalog.yml` layer definition:
  ```yaml
  # Legacy
  layer: raw
  # Modern (1.0+)
  metadata:
    kedro-viz:
      layer: raw
  ```

## 4. CLI arguments

- `--namespace` → `--namespaces` (accepts comma-separated values).
- `kedro catalog create` → removed.

## 5. API renames

- `ModularPipelineError` → `PipelineError`
- `extra_params` → `runtime_params` (inside `KedroSession`).
- `session_id` → `run_id` (in methods and hooks).
