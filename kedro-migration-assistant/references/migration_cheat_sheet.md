# Kedro Migration Cheat Sheet

## 1. Pipeline Classes (The most frequent error)
- **Old (0.19.x):** `from kedro.pipeline.modular_pipeline import node, pipeline`
- **New (1.x):** `from kedro.pipeline import Node, Pipeline`
- **Change:** `node(func=f, inputs="i", outputs="o")` -> `Node(func=f, inputs="i", outputs="o")`
- **Change:** `pipeline([nodes], pipe=...)` -> `Pipeline(nodes=[nodes])` (Note the argument name `nodes`).

## 2. Dataset Naming (Dataset vs DataSet)
- **Problem:** Kedro 1.0+ is strict about `Dataset` casing.
- **Fix:** Search and replace `DataSet` with `Dataset` across all `catalog.yml` and Python files.
- **Examples:** `pandas.CSVDataSet` -> `pandas.CSVDataset`, `pickle.PickleDataSet` -> `pickle.PickleDataset`.

## 3. Catalog & Configuration
- `KedroDataCatalog` -> `DataCatalog`
- `ConfigLoader` / `TemplatedConfigLoader` -> `OmegaConfigLoader`
- `catalog.yml` layer definition:
  ```yaml
  # Old
  layer: raw
  # New
  metadata:
    kedro-viz:
      layer: raw
  ```

## 4. CLI Arguments
- `--namespace` -> `--namespaces` (Accepts comma-separated values).
- `kedro catalog create` -> Removed.

## 5. API Renames
- `ModularPipelineError` -> `PipelineError`
- `extra_params` -> `runtime_params` (Inside `KedroSession`).
- `session_id` -> `run_id` (In methods and hooks).
