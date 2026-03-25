---
name: kedro-hooks-plugins
description: Comprehensive guide for developing Kedro Hooks and Plugins. Use this skill when the user asks about injecting custom logic during pipeline execution (e.g., before_node_run, on_pipeline_error), building notification systems, integrating tools like MLflow, or overriding core Kedro behaviors like creating Custom Node Caching Mechanisms and Custom Runners.
metadata:
  author: Francisco Muñoz (@framunoz)
  version: "1.0.0"
  source: https://github.com/framunoz/my-skills
  inspiration: The [Kedro MCP server](https://docs.kedro.org/en/stable/develop/vibe_coding_with_mcp/)
---

# Kedro Hooks & Plugins Developer Guide

Kedro's hook system allows you to inject custom behavior into the execution lifecycle of a pipeline. This skill contains the architectural knowledge required to build robust plugins.

Determine the user's intent and read the corresponding resource file located in the `references/` directory next to this `SKILL.md`:

### 1. 🎣 Hook Lifecycle & Architecture (`references/hooks_architecture.md`)
**When to read:** Whenever you need to create a new Hook, understand at what point a specific hook triggers, or build notifications (e.g., Slack alerts on failure), data validation (e.g., Great Expectations before a node runs), or experiment tracking (MLflow).
**What it contains:** 
- The 7 core Kedro hook specifications (`after_catalog_created`, `before_pipeline_run`, `before_node_run`, `after_node_run`, `after_pipeline_run`, `on_node_error`, `on_pipeline_error`).
- How to register hooks in `settings.py`.

### 2. ⚡ Dynamic Caching & Node Bypassing (`references/caching_strategies.md`)
**When to read:** Whenever the user asks how to "skip" a node, implement a cache system, prevent an expensive model from rerunning, or modify the Runner.
**What it contains:**
- The limitation of Hooks (Why you can't just "skip" a node in `before_node_run`).
- The 3 supported patterns for Caching (Node-level logic, Plugins, Custom Runners).

### 3. 📂 Practical Examples (`assets/`)
**When to read:** Whenever you need to implement a Hook or Custom Runner and want to copy a boilerplate template.
**Available files:**
- `assets/node_timing_hook.py`: Complete implementation of `@hook_impl` decorators tracking node execution time.
- `assets/data_validation_hook.py`: Implementation of `before_node_run` and `after_node_run` to inspect Pandas DataFrames, enforcing column schemas, data types, and null checks dynamically.
- `assets/time_based_cache_runner.py`: A `SequentialRunner` subclass built to bypass Node execution completely if its output file is `< 24 hours` old (Strategy C).

---

## 💡 Core Principles of Hook Architecture
1. **Treat hooks as pure lifecycle spectators**: Hooks are designed to observe pipeline execution (like telemetry or simple validation). Mutating the `catalog` or `pipeline` objects inside a hook introduces hidden side effects that make the project extremely difficult to debug. Avoid modifications unless specifically building advanced dynamic workflow plugins.
2. **Isolate hook failures safely**: Kedro executes hooks synchronously. If a hook crashes (e.g., a network timeout while sending an alert to Slack in `on_node_error`), it will crash the entire pipeline run. Always wrap external API logic inside a `try/except` block to log warnings without interrupting the user's data process.
3. **Correctly register handlers**: The framework determines which methods intercept signals via the `@hook_impl` decorator imported from `kedro.framework.hooks`.
4. **Rethink "skipping" nodes**: Hooks do not govern the execution DAG—the Runner does. Consequently, you cannot gracefully "skip" a node simply by intercepting `before_node_run`. Doing so denies outputs downstream and causes unresolved dependency errors. If skipping logic is requested, consult `caching_strategies.md` to design a Custom Runner or caching pattern instead.
