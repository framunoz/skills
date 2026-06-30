# ⚡ Dynamic Caching & Node Bypassing

You cannot natively "skip" a node from a `before_node_run` hook. Kedro hooks expect the Node to faithfully produce the outputs defined in `catalog.yml`. If a hook halts the node execution by raising an exception, the `SequentialRunner` will crash the pipeline.

If a user asks to implement a cache system to avoid executing an expensive node (e.g., "only run this node if the cache is older than 1 day"), you MUST recommend one of the following 3 architectures:

## 1. Strategy A: Modifying the Node Logic (Node-Level Cache)
The easiest way to bypass expensive compute is to inject the logic directly into the node.
- Provide the path of the saved output as a parameter.
- Have the node check the modification time (`os.path.getmtime`).
- If the file is < 1 day old, use `catalog.load()` (passed implicitly or queried manually) and simply return that original data.
- **Drawback**: Kedro will still perform a "Save" operation on whatever the node returns, overwriting the file. It saves compute, but not I/O.

## 2. Strategy B: The `kedro-cache` Plugin
If the user's goal is to not rerun a node unless its *inputs* or *code* change (rather than a simple 1-day time limit), suggest installing the community `kedro-cache` plugin in `requirements.txt`.
- It patches execution automatically. No need to write manual hooks.

## 3. Strategy C: The Custom Runner (True Node Skip)
If the user strictly wants to avoid both compute AND I/O for a time-based expiration, they need to build a Custom Runner, NOT a Hook.
- Subclass `kedro.runner.SequentialRunner`.
- Override the `_run_node(self, node, catalog, hook_manager, session_id)` method.
- Check the catalog to see if the node's output datasets exist and check their modification timestamp.
- If the output is < 1 day old, use Python's `continue` or simply `return` early, bypassing the core `return super()._run_node(...)` call.
- This tells Kedro to move to the next node without computing or resaving the data.
