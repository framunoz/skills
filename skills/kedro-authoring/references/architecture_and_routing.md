# 🏗️ Kedro Architecture & Routing

## 1. Directory Structure

A standard Kedro 1.0+ project should follow this organization:
```
my_project/
├── conf/
│   ├── base/
│   │   ├── catalog.yml
│   │   ├── parameters.yml
│   │   └── parameters_*.yml (e.g. parameters_data_science.yml)
│   └── local/ (Git-ignored)
├── data/
│   ├── 01_raw/
│   ├── 02_intermediate/
│   ├── 03_primary/
│   ├── 04_feature/
│   ├── 05_model_input/
│   ├── 06_models/
│   ├── 07_model_output/
│   └── 08_reporting/
└── src/
    └── my_project/
        ├── pipelines/
        │   ├── <pipeline_name>/
        │   │   ├── __init__.py
        │   │   ├── nodes.py
        │   │   └── pipeline.py
        └── pipeline_registry.py
```

### Environments & Secrets
- **`conf/base`**: Store all shared defaults (e.g., standard `catalog.yml`, default `parameters.yml`).
- **`conf/local`**: Store everything machine-specific or sensitive (credentials, paths for local execution). This folder is git-ignored and **MUST NEVER** be committed.

## 2. Technical Implementation Standards

### Node Implementation Requirements
- **Pure functions only**: No side effects (e.g., no `df.to_csv()` or `plt.savefig()`). I/O must be handled strictly by the Data Catalog.
- **Single Output Rule**: Nodes must strive for exactly ONE output whenever possible to maintain clean graph structures.
- **Type Hints**: Clear type hints are required for all standard inputs and outputs (e.g., `pd.DataFrame`, `t.Dict`).
- **Parameter References**: Use specific parameter prefixes `params:group_name` rather than passing the entire `"parameters"` dictionary unless the function requires many unrelated parameters.

### Project Setup & Pipeline Standards
- **Project Structure Setup**: When creating a new project from scratch, use the strictest command flag configuration to avoid bloated boilerplate: `kedro new --name <PROJECT> --tools=data,lint,test --example=no --telemetry=no`.
- **Pipeline Structure Setup**: Use `kedro pipeline create <name>` CLI only (never manual folder creation).
- **Node & Pipeline Definitions**: Instantiate nodes and pipelines using `kedro.pipeline.Node` and `kedro.pipeline.Pipeline` classes.
- **Pipeline Registry**: Explicitly register all generated pipelines in `src/my_project/pipeline_registry.py`, combining smaller cohesive pipelines into larger overarching runs (like `__default__`).
- **Namespaces**: Always use the `namespace` argument when assigning nodes to a pipeline or when registering them in the `pipeline_registry.py`. E.g., `pipeline(pipe, namespace="data_science")`. Namespaces automatically encapsulate nodes and their intermediate datasets, preventing naming collisions between different models or pipeline branches. Remember that to run a namespace using the Kedro 1.0+ CLI, you must use `--namespaces=<name>`.
- **Tags**: Liberally apply tags to your `Node` objects (e.g., `Node(..., tags=["memory_heavy", "cpu_intensive"])`). Tags are incredibly useful for segmenting pipeline execution without creating entirely separate pipelines. This allows running subsets of tasks via `kedro run --tags=memory_heavy`.
- **Logging**: Global logging configurations are managed in an independent `logging.yml` injected via the `KEDRO_LOGGING_CONFIG` environment variable in 1.0+. Use standard `logging.getLogger(__name__)` inside nodes.

## 3. Quality Assurance Checklist
When completing a Kedro execution task, review the following before delivery:
- [ ] Pipeline was created via CLI.
- [ ] Nodes are pure functions WITH type hints.
- [ ] Catalog is explicit, and no `node` performs I/O operations directly.
- [ ] Parameters are logically grouped in `parameters.yml`.
- [ ] Dependencies added are strictly necessary and installed/pinned correctly in `requirements.txt` / `pyproject.toml`.
- [ ] Any deviation from standard Kedro conventions is fully documented.

## 4. Useful Documentation Links
- [Kedro Core Documentation](https://docs.kedro.org/)
- [Kedro Pipeline Node Tags Reference](https://docs.kedro.org/en/stable/nodes_and_pipelines/run_a_pipeline.html#run-a-pipeline-by-tags)
