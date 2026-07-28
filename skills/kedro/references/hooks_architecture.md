# 🎣 Hook Lifecycle & Architecture

Kedro allows you to hook into 7 specific events during the execution of a pipeline. To create a hook, you define a class containing methods named exactly as the specifications, decorated with `@hook_impl`.

## 1. The Hook Specifications

- **`after_catalog_created(catalog, conf_catalog, conf_creds, ...)`**: Runs right after the `DataCatalog` is instantiated. Useful for programmatically adding datasets or validating the catalog.
- **`before_pipeline_run(run_params, pipeline, catalog)`**: Runs before any node executes. Useful for setting up global state (e.g., starting an MLflow run).
- **`before_node_run(node, catalog, inputs, is_async, run_id)`**: Runs right before a node executes. Useful for Data Validation (e.g., checking if `inputs` has nulls before training). Note: You *can* modify `inputs` here by returning a dictionary, but you *cannot* cleanly skip the node.
- **`after_node_run(node, catalog, inputs, outputs, is_async, run_id)`**: Runs immediately after a node finishes. Useful for logging metrics, profiling execution time, or evaluating outputs.
- **`on_node_error(error, node, catalog, inputs, is_async, run_id)`**: Triggered if a node raises an Exception. Perfect for sending alerts (Slack/Teams).
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

## 3. Pluggy gotchas (why hooks silently misbehave)

Kedro hooks run on `pluggy`, which wires your implementation to the spec **by argument name**, not by position. Two consequences trip people up constantly:

- **Declare only the arguments you actually use.** You don't have to accept the full spec signature — pick a subset and pluggy injects just those. `def before_node_run(self, node, inputs):` is perfectly valid and cleaner than dragging along `catalog`, `is_async`, `run_id` you never touch. Conversely, the names you *do* declare must match the spec exactly (e.g. `run_id`, not `session_id` — see `migration_and_syntax.md`), or pluggy raises an "unknown argument" error at registration.
- **Never give hook arguments default values.** Because injection is name-based, a default like `def before_node_run(self, node, inputs=None):` interferes with how pluggy supplies the argument and it ends up not populated as you expect. Keep hook parameters plain and required; store *your own* configuration (thresholds, required columns, webhook URLs) as constructor arguments or class attributes instead.

```python
class FeatureValidationHook:
    def __init__(self, required_columns=("user_id", "timestamp")):
        self._required = set(required_columns)  # config lives on the instance, not in hook args

    @hook_impl
    def before_node_run(self, node: Node, inputs: Dict[str, Any]) -> None:  # only what we use, no defaults
        ...
```
