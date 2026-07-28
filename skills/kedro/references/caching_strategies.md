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

## 3. Strategy C: Native Pipeline Slicing (Avoid Both Compute AND I/O)
If the user strictly wants to avoid both compute AND I/O for an expensive node, prefer Kedro's **native CLI slicing** over any custom runner. It is the simplest correct approach and relies only on the public API:

1. Persist the expensive node's output to the catalog once (e.g. a `pickle.PickleDataset` or `pandas.ParquetDataset` entry in `catalog.yml`).
2. On subsequent runs, skip the expensive node entirely by starting *after* it:
   ```bash
   kedro run --from-nodes=<node_after_the_expensive_one>
   ```
   The skipped node never executes (zero compute, zero save); Kedro simply loads the persisted output from the catalog as an input to the downstream nodes.
- Alternatives for slicing: `kedro run --nodes=<a,b,c>` (run only these), `--to-nodes` / `--to-outputs` (stop early). All avoid both compute and I/O for the excluded nodes.
- For automatic, content-aware invalidation (rather than manual slicing), use the `kedro-cache` plugin from Strategy B.

> Avoid hand-rolling a custom runner that overrides internal methods to "skip" nodes. In Kedro 1.0+ the runner internals (method names, signatures, the catalog's private dataset access) are not a stable extension point, so such code breaks silently across versions. Native slicing and `kedro-cache` cover this need without touching internals.
