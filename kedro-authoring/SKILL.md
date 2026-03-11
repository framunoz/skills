---
name: kedro-authoring
description: Comprehensive guidance and context for developing with Kedro (Pipelines, Nodes, Catalog). Use this skill whenever the user mentions writing Kedro pipelines, adding Kedro nodes, modifying the data catalog `catalog.yml`, or requests help with Kedro project structures, best practices, or building data workflows. Activate this skill even if the user only mentions general terms like "nodes," "pipelines," or "parameters" in the context of Kedro.
---

# Kedro Authoring

This skill provides comprehensive context for the Kedro framework, helping you write robust, production-ready data pipelines strictly for Kedro 1.0+ while avoiding common anti-patterns.

Depending on the exact user request, **you MUST use the `view_file` tool** to read the bundled reference resource below. Do not guess the Kedro syntax without consulting this reference first.

## 📚 Bundled Resources

Determine the user's intent and read the corresponding resource file located in the `references/` directory next to this `SKILL.md`:

### 1. 🏗️ Architecture & Routing (`references/architecture_and_routing.md`)
**When to read:** Whenever you are writing new Kedro code, creating new Nodes, drafting Pipelines, or determining where a certain piece of code belongs.
**What it contains:** 
- The standard Kedro directory structure.
- Strict technical implementation standards (Pure functions, Single Output Rule, Kedro 1.0+ class usage).
- Guidance on using `namespaces` and `tags` to encapsulate and segment logic.
- A Quality Assurance (QA) Checklist to verify your work before delivering to the user.

### 2. 🗂️ Data Catalog & Layering Standards (`references/data_catalog_standards.md`)
**When to read:** Whenever you are mapping inputs/outputs, modifying `catalog.yml`, or determining which folder inside `data/` a dataset belongs to.
**What it contains:**
- The data layering definition for `01_raw` through `08_reporting`.
- A reference table for Kedro 1.0+ dataset classes (e.g., `pandas.CSVDataset`, `pandas.ParquetDataset`).

### 3. ⚙️ Parameter Framework (`references/parameter_framework.md`)
**When to read:** Whenever you are modifying `parameters.yml` or deciding whether a variable should be hardcoded in python versus injected.
**What it contains:**
- The decision matrix for what goes in `parameters.yml` (e.g., experimentation variables, logic rules) vs what goes in `nodes.py` (schemas, hard constants).

### 4. 📂 Practical Examples (`assets/`)
**When to read:** Whenever you need an exact YAML template for a specific dataset type or advanced configuration.
**What it contains:** 
- Individual YAML files for Pandas (CSV, Parquet, Excel), Pickle, JSON, YAML, visualization outputs (Matplotlib, Plotly), API requests, and SQL databases.
- `advanced_configurations.yml`: A showcase of `versioned: true`, `copy_mode: assign`, cloud `fs_args`, and `metadata.kedro-viz`.

### 5. 🛠️ Automation Scripts (`scripts/`)
**When to use:** Whenever you want to verify your changes or analyze an existing codebase for technical debt.
**Available scripts:**
- `scripts/validate_project.py`: A Python tool that scans the `src/` directory for Kedro anti-patterns (e.g., direct I/O like `.to_csv()`, deprecated wrapper imports, or legacy `DataSet` casing). Execute this script via the `run_shell_command` tool to get an immediate audit of the project's health.

---

## 💡 Core Principles of Kedro Architecture
1. **Nodes act as pure functions without I/O side effects**: Kedro's architecture relies on the Data Catalog (`conf/base/catalog.yml`) to govern data loading and saving. Nodes should merely accept variables and return variables. Calling `.to_csv()` or `.savefig()` inside a node breaks the pipeline abstraction and disables Kedro's automated state tracking, caching, and visualization capabilities. Let the Catalog handle it.
2. **Leverage CLI generation for structured project scaffolding**: Instead of manually creating pipeline directories, executing `kedro pipeline create <name>` ensures the framework's boilerplate (like `nodes.py` and `pipeline.py` templates) is generated correctly and registered.
3. **Enforce Kedro 1.0+ standards for forward compatibility**: 
    - To remain compatible with modern Kedro, use the explicitly capitalized `Node` and `Pipeline` classes directly from `kedro.pipeline`.
    - Avoid the lowercase wrapper functions `kedro.pipeline.node()` and `kedro.pipeline.pipeline()`, as they are deprecated and will cause compatibility errors.
    - Consistently end your catalog datasets with `Dataset` (not `DataSet`).
4. **Apply Tags and Namespaces for granular scalability**: As pipelines grow, proactively applying `tags` to `Node` objects and `namespace` strings to pipelines (in `pipeline_registry.py`) prevents data name collisions and allows the user to run specific slices of the Directed Acyclic Graph (DAG) with ease.

*If you are unsure about any syntax or pattern, STOP and read the corresponding file in the `references/` directory.*

## 🔗 External Reference Links
If the user demands more specific advanced use cases not covered in the bundled resources, suggest these official sources:
- **Core Docs**: [https://docs.kedro.org/](https://docs.kedro.org/)
- **Data Catalog & Datasets**: [https://docs.kedro.org/en/stable/data/data_catalog.html](https://docs.kedro.org/en/stable/data/data_catalog.html)
- **Visualizing with Kedro-Viz**: [https://docs.kedro.org/projects/kedro-viz/en/stable/](https://docs.kedro.org/projects/kedro-viz/en/stable/)

