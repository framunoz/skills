# 🎣 Hook Lifecycle & Architecture

Kedro allows you to hook into 7 specific events during the execution of a pipeline. To create a hook, you define a class containing methods named exactly as the specifications, decorated with `@hook_impl`.

## 1. The Hook Specifications

- **`after_catalog_created(catalog, conf_catalog, conf_creds, ...)`**: Runs right after the `DataCatalog` is instantiated. Useful for programmatically adding datasets or validating the catalog.
- **`before_pipeline_run(run_params, pipeline, catalog)`**: Runs before any node executes. Useful for setting up global state (e.g., starting an MLflow run).
- **`before_node_run(node, catalog, inputs, is_async, session_id)`**: Runs right before a node executes. Useful for Data Validation (e.g., checking if `inputs` has nulls before training). Note: You *can* modify `inputs` here by returning a dictionary, but you *cannot* cleanly skip the node.
- **`after_node_run(node, catalog, inputs, outputs, is_async, session_id)`**: Runs immediately after a node finishes. Useful for logging metrics, profiling execution time, or evaluating outputs.
- **`on_node_error(error, node, catalog, inputs, is_async, session_id)`**: Triggered if a node raises an Exception. Perfect for sending alerts (Slack/Teams).
- **`after_pipeline_run(run_params, run_result, pipeline, catalog)`**: Triggered when the entire pipeline finishes successfully. Useful for closing trackers or sending success emails.
- **`on_pipeline_error(error, run_params, pipeline, catalog)`**: Triggered if the pipeline fails overall.

## 2. Implementing and Registering a Hook

### Step A: Define the Hook Class
```python
import logging
from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node
from typing import Any, Dict

logger = logging.getLogger(__name__)

class NodeTimingHook:
    @hook_impl
    def before_node_run(self, node: Node) -> None:
        logger.info(f"🚀 Starting execution of node: {node.name}")

    @hook_impl
    def on_node_error(self, error: Exception, node: Node) -> None:
        logger.error(f"❌ Node {node.name} failed with error: {error}")
        # Add Slack API call here (wrapped in try/except)
```

### Step B: Register the Hook in `settings.py`
To make the hook active, simply instantiate it in `src/my_project/settings.py` inside the `HOOKS` tuple:
```python
# settings.py
from my_project.hooks import NodeTimingHook

HOOKS = (NodeTimingHook(),)
```
