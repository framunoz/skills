---
name: kedro
description: Comprehensive guidance for Kedro 1.0+ projects. Use proactively for explicit Kedro terms or files (for example `kedro`, `catalog.yml`, `parameters.yml`, hooks, Kedro-Viz, or `kedro pipeline`); creating, migrating, upgrading, or extending Kedro pipelines, nodes, catalogs, hooks, or plugins; and productionizing a data-science notebook or analysis script into Kedro nodes, pipelines, and catalog datasets. Do not trigger on isolated generic terms such as node, pipeline, parameter, or dataset without clear Kedro context.
license: MIT
compatibility: Targets Kedro 1.0+. Assumes a Python project using `kedro` and `kedro-datasets`.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: "2.0.0"
  source: https://github.com/framunoz/skills
  inspiration: The Kedro MCP server (https://docs.kedro.org/en/stable/develop/vibe_coding_with_mcp/)
  tags: data-engineering, kedro, pipelines, python
---

# Kedro

This skill provides comprehensive context for building robust, production-ready data pipelines strictly for **Kedro 1.0+**, covering four areas: authoring new pipelines, migrating legacy projects, extending Kedro with hooks/plugins, and converting notebooks into Kedro.

The reference material lives in `references/` and `assets/` next to this `SKILL.md`. **Use the `view_file` tool to read a reference before writing code** — do not guess Kedro syntax from memory, because the API changed significantly in 1.0+ and older patterns are easy to confuse.

## ⚠️ Step 0 — ALWAYS read this first

Before doing anything else — regardless of the task — read **`references/migration_and_syntax.md`**.

Kedro 1.0+ renamed core classes, datasets, CLI flags, and config loaders relative to older (pre-1.0) versions. The most common failure across *every* Kedro task is silently mixing legacy syntax (e.g. `node()`, `pipeline()`, `CSVDataSet`, `--namespace`) with modern syntax (`Node`, `Pipeline`, `CSVDataset`, `--namespaces`). Reading this file first calibrates you on the correct 1.0+ syntax so you don't introduce deprecated patterns into new code or miss them during a migration. It is short and applies whether you are authoring, migrating, hooking, or converting.

## 🧭 Router — read by intent

After Step 0, identify what the user is trying to do and read the matching references:

| User intent | Read first | Then also consult |
| :--- | :--- | :--- |
| **Build / write** a new pipeline, node, or catalog | `references/architecture.md` | `references/data_catalog.md`, `references/parameters.md`, `assets/catalog/` |
| **Migrate / upgrade** a project or fix deprecated syntax | `references/migration_and_syntax.md` (already read in Step 0) | `references/architecture.md` for post-migration validation |
| **Extend** Kedro with hooks or plugins | `references/hooks_architecture.md` | `references/caching_strategies.md`, `assets/hooks/` |
| **Track experiments / register models** with MLflow | `references/mlflow_integration.md` | `references/hooks_architecture.md`, `references/data_catalog.md`, `assets/mlflow/` |
| **Skip / cache** an expensive node | `references/caching_strategies.md` | `references/hooks_architecture.md` |
| **Convert** a Jupyter notebook / `.qmd` into Kedro | `references/notebook_conversion.md` | `references/architecture.md`, `references/data_catalog.md`, `references/parameters.md` |
| **Validate** project health / audit technical debt | `scripts/validate_project.py` (run it) | `references/architecture.md` QA checklist |

## 📂 Bundled resources

- **`references/migration_and_syntax.md`** — Legacy → 1.0+ syntax map (classes, datasets, catalog, CLI, API renames, config loader). The Step 0 read.
- **`references/architecture.md`** — Directory structure, technical standards (pure functions, single-output rule, type hints), namespaces & tags, QA checklist.
- **`references/data_catalog.md`** — Data layering (`01_raw` → `08_reporting`), dataset type reference table, advanced config (versioning, `copy_mode`, `fs_args`, Kedro-Viz metadata, factories, partitions).
- **`references/parameters.md`** — Decision matrix for `parameters.yml` vs hardcoded constants, plus `OmegaConfigLoader` interpolation.
- **`references/hooks_architecture.md`** — The 7 hook specs, `@hook_impl`, and registration in `settings.py`.
- **`references/caching_strategies.md`** — Why hooks can't "skip" nodes, and the supported patterns (node-level cache, `kedro-cache` plugin, native CLI pipeline slicing).
- **`references/notebook_conversion.md`** — The 6-step Statement of Work (SOW) workflow plus the SOW template for converting notebooks.
- **`references/mlflow_integration.md`** — MLflow experiment tracking & model registry: the `kedro-mlflow` plugin (install, version compatibility, `mlflow.yml`, catalog datasets, CLI), the native-SDK-in-hooks path, and the model registry lifecycle (versioning, stages vs aliases).
- **`assets/catalog/`** — Copy-pasteable `catalog.yml` snippets per dataset type and an `advanced_configurations.yml` showcase.
- **`assets/hooks/`** — Production-ready hook examples: `node_timing_hook.py`, `data_validation_hook.py`, `mlflow_native_hook.py`.
- **`assets/mlflow/`** — `mlflow.yml` config template and `catalog_mlflow.yml` (MLflow dataset snippets: artifacts, metrics, model tracking, model registry).
- **`scripts/validate_project.py`** — Scans `src/` for anti-patterns (direct I/O, deprecated imports, legacy `DataSet` casing). Run it via `run_shell_command` to audit a project.

## 💡 Core principles (apply across all tasks)

1. **Nodes are pure functions without I/O side effects.** Kedro's Data Catalog (`conf/base/catalog.yml`) governs all loading and saving. Nodes accept variables and return variables. Calling `.to_csv()` or `.savefig()` inside a node breaks the pipeline abstraction and disables state tracking, caching, and visualization. Let the Catalog handle it.
2. **Use Kedro 1.0+ syntax consistently** (see Step 0): capitalized `Node`/`Pipeline` classes from `kedro.pipeline`, dataset classes ending in `Dataset`, `--namespaces` (plural) on the CLI, and `OmegaConfigLoader`. Mixing in legacy forms is the #1 cause of failures.
3. **Leverage the CLI for scaffolding.** Use `kedro pipeline create <name>` rather than hand-creating directories so boilerplate is generated and registered correctly. For new projects: `kedro new --name <PROJECT> --tools=data,lint,test --example=no --telemetry=no`.
4. **Apply tags and namespaces for scalability.** As pipelines grow, tag `Node` objects and namespace pipelines to prevent name collisions and allow running slices of the DAG.

_If you are unsure about any syntax or pattern, STOP and read the corresponding file in `references/` before writing code._

## 🔗 External reference links

For advanced cases not covered here, point the user to the official sources:

- **Core docs**: https://docs.kedro.org/
- **Data Catalog & Datasets**: https://docs.kedro.org/en/stable/data/data_catalog.html
- **Kedro-Viz**: https://docs.kedro.org/projects/kedro-viz/en/stable/
