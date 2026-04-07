---
name: kedro-migration-assistant
description:
  Technical guide for upgrading, migrating, or resolving versioning errors
  in Kedro projects. Use this skill whenever the user explicitly asks to upgrade a
  Kedro project, migrate from Kedro 0.18 or 0.19 to Kedro 1.0+, or asks about deprecated
  Kedro syntax and API changes (e.g., KedroDataCatalog, ModularPipelineError, `--namespace`).
metadata:
  author: Francisco Muñoz (@framunoz)
  version: 1.0.1
  source: https://github.com/framunoz/skills
  inspiration: The [Kedro MCP server](https://docs.kedro.org/en/stable/develop/vibe_coding_with_mcp/)
  tags: data-engineering, kedro, pipelines, python
  related-with:
    skills:
      - kedro-authoring
      - kedro-hooks-plugins
      - kedro-notebook-converter
---

# Kedro Migration Assistant

This skill helps resolve breaking changes when migrating Kedro projects to version 1.0+.

## 📚 Bundled Resources

Determine the user's intent and read the corresponding resource file located in the `references/` directory next to this `SKILL.md`:

### 1. 🚀 Migration Cheat Sheet (`references/migration_cheat_sheet.md`)

**When to read:** Whenever you need to fix syntactical errors (Node/Pipeline classes, DataSet vs Dataset casing) or perform a whole project migration.
**What it contains:**

- Quick comparison of old vs new syntax.
- Common dataset naming corrections.
- Catalog and configuration resolution steps.
- CLI execution changes.

---

## 💡 Core Principles of Kedro Migration

1. **Capitalization Matters**: Kedro 1.0+ transitioned from functional wrappers (`node()`, `pipeline()`) to explicit classes (`Node`, `Pipeline`). Using the wrong case is the #1 cause of migration failures.
2. **Dataset Normalization**: All datasets must end in `Dataset` (not `DataSet`).
3. **Namespace Pluralization**: The `--namespace` argument is gone; use `--namespaces` instead, even for a single value.
4. **Configuration Resolution**: Legacy `ConfigLoader` implementations must be replaced by `OmegaConfigLoader` which supports `${...}` interpolation.

_If you are unsure about a specific API change, read `references/migration_cheat_sheet.md` before applying code modifications._
