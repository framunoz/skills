# Pipelines: nodes, composition, namespaces, registry, slicing, typed params

Kedro 1.7.0. "(verified on 1.7.0)" = run in a scratch spaceflights project; the rest comes from
the official docs (`build/*`, `configure/how_to_use_parameters_and_credentials`).

## Imports: `Node` vs `node()`, `Pipeline` vs `pipeline()`

```python
from kedro.pipeline import Node, Pipeline          # what the 1.x docs and templates use
from kedro.pipeline import node, pipeline          # thin factory functions, same signatures
```

`node(...)` returns a `Node`, and `pipeline(...)` returns `Pipeline(...)`. Neither is deprecated —
only the old import path `kedro.pipeline.modular_pipeline` was removed (1.0):
no warning with `-W always` (verified on 1.7.0). Pick one style per project. The
`kedro pipeline create` template uses `Node`/`Pipeline`.

## Nodes

```python
Node(func, inputs, outputs, *, name=None, tags=None, confirms=None, namespace=None, preview_fn=None)
```

Everything after `outputs` is **keyword-only**.

| `inputs` | Function called as |
|---|---|
| `None` | `f()` |
| `"a"` | `f(a)` |
| `["a", "b"]` | `f(a, b)` (positional; also feeds `*args`) |
| `{"x": "a", "y": "b"}` | `f(x=a, y=b)` (keyword; feeds `**kwargs`) |
| `"params:model_options"` | one parameter key (nested keys: `params:model_options.test_size`) |
| `"parameters"` | the whole parameters dict |

| `outputs` | Function must return |
|---|---|
| `None` | nothing. A returned value is dropped with `UserWarning: Node 'r' returned a value of type 'int', but the node is defined with outputs=None...` (verified on 1.7.0) |
| `"a"` | one object |
| `["a", "b"]` | list/tuple of the same length, otherwise `ValueError: ... The node definition contains a list of outputs ['c', 'd'], whereas the node function returned a 'int'.` (verified on 1.7.0) |
| `{"k1": "a", "k2": "b"}` | dict with keys `k1`, `k2` |

- `Node(f, None, None)` is invalid: `Invalid Node definition: it must have some 'inputs' or 'outputs'.`
- A wrong input count fails when the node is built: `TypeError: Inputs of 'add' function expected ['a', 'b'], but got ['a']` (verified on 1.7.0).
- Names and tags may only contain letters, digits, `-`, `_` and `.`, otherwise
  `ValueError: 'bad name!' is not a valid node name. It must contain only letters, digits, hyphens, underscores and/or fullstops.` (verified on 1.7.0).
- Avoid `.` in **dataset** names: it is reserved for namespaces, and Kedro emits a `UserWarning`
  ("dot notation is reserved for automatic namespacing").
- Testing: `node.run({"a": 1, "b": 2})` returns `{"s": 3}`. `node(a=1, b=2)` also works:
  `__call__` takes **kwargs. The docs' `adder_node(dict(a=2, b=3))` raises `TypeError` (verified on 1.7.0).

### Default node names: name every node

Since 1.0, an unnamed node is called `<func_name>__<8-hex SHA-256>`. The hash covers the
function, inputs and outputs (verified on 1.7.0):

```text
Node(add, ["a","b"], "s")  -> add__917d8097
Node(add, ["a","c"], "s")  -> add__257b149d     # rename an input and the name changes
kedro registry describe reporting
- compare_passenger_capacity_exp__1d605aeb (compare_passenger_capacity_exp)
```

`--nodes add` does not match `add__917d8097`: `ValueError: Pipeline does not contain nodes named ['add'].`
(verified on 1.7.0). Unnamed nodes therefore break `--nodes`, `--from-nodes`, `--to-nodes`,
run configs and deployment scripts as soon as their wiring changes. **Always pass `name=`.**
The log line `Running node: make_numbers: ...` shows the name you passed, without the namespace
prefix; `kedro registry describe` shows the full name.

### Node functions

- Keep them pure: data in, data out. No catalog access, no file I/O, no reading global config.
  I/O belongs to the catalog. Pure functions can be tested with `node.run({...})`, and
  ParallelRunner needs them picklable.
- Use module-level functions. Lambdas, closures and nested functions break `ParallelRunner`
  (see `running.md`). With `functools.partial`, Kedro warns that partials have no `__name__`;
  use `functools.update_wrapper`.
- Node-level `namespace="grp"` only prefixes the **node name** (`grp.add__917d8097`). Datasets
  are not renamed (verified on 1.7.0). Use it for Kedro-Viz grouping, not for reuse.

### Generator nodes

A node function that `yield`s is streamed: **each yielded value is a separate `save()`** on the
output dataset (verified on 1.7.0: a custom dataset received `[0, 10, 20]`). Consequences:

- The output must be a dataset that appends (custom `_save` in append mode, or a chunk-aware
  dataset). A plain file dataset gets overwritten on every chunk.
- A `MemoryDataset` output keeps **only the last chunk**. The downstream node received `20`, not
  all three chunks (verified on 1.7.0).
- Multi-output generators yield tuples: `yield a, b` with `outputs=["p", "q"]`.
- Since 1.4 only real generator functions are streamed. Other iterable return values are saved
  as-is.

## Pipelines

```python
Pipeline(nodes, *, inputs=None, outputs=None, parameters=None, tags=None,
         namespace=None, prefix_datasets_with_namespace=True)
```

`nodes` may mix `Node`s and `Pipeline`s, or be a single `Pipeline`. Execution order comes from
the data dependencies, not from list order.

| Operation | Meaning (verified on 1.7.0, source: `pipeline.py`) |
|---|---|
| `p1 + p2` / `p1 \| p2` | union of nodes (identical `Node` objects are de-duplicated) |
| `p1 - p2` | nodes of `p1` that are not in `p2` |
| `p1 & p2` | nodes present in both |
| `sum(pipes.values())` | works (`__radd__` accepts `0`) |
| `p.inputs()` / `p.outputs()` | free inputs / terminal outputs |
| `p.all_inputs()` / `p.all_outputs()` / `p.datasets()` | every name involved |
| `p.describe()` | prints the execution order |
| `p.nodes` | topologically sorted list |
| `p.tag("x")` | new pipeline with an extra tag on every node |
| `p.group_nodes_by(group_by="namespace")` | `list[GroupedNodes]` for deployment plugins (replaced `grouped_nodes_by_namespace()` in 1.0) |

Validation errors (verified on 1.7.0):

```text
ValueError: Pipeline nodes must have unique names. The following node names appear more than once:
Free nodes:
  - x
You can name your nodes using the last argument of 'node()'.
OutputNotUniqueError: Output(s) ['c'] are returned by more than one nodes. Node outputs must be unique.
Circular dependencies exist among these items: [...]
```

### Reuse: mapping and namespaces

`inputs` / `outputs` / `parameters` accept a `str`, a `set` (keep these names un-prefixed) or a
`dict` (`{old: new}` rename). Parameter keys keep their `params:` prefix in the mapping.

What `namespace="ds1"` does to `Node(f, ["raw", "params:opts"], "mid", name="f_node")` + `Node(g, "mid", "out", name="g_node")`
(verified on 1.7.0):

| Pipeline(...) arguments | node name | inputs | outputs |
|---|---|---|---|
| `namespace="ds1"` | `ds1.f_node` | `ds1.raw`, `params:ds1.opts` | `ds1.mid` |
| `+ inputs={"raw"}` | `ds1.f_node` | `raw`, `params:ds1.opts` | `ds1.mid` |
| `+ parameters={"params:opts": "params:opts_1"}` | `ds1.f_node` | `ds1.raw`, `params:opts_1` | `ds1.mid` |
| `+ outputs={"out": "final"}` | `ds1.g_node` | `ds1.mid` | `final` |
| `prefix_datasets_with_namespace=False` | `ds1.f_node` | `raw`, `params:opts` | `mid` |
| nested `Pipeline(Pipeline(p, namespace="inner"), namespace="outer")` | `outer.inner.f_node` | `outer.inner.raw`, `params:outer.inner.opts` | `outer.inner.mid` |
| input `"parameters"` (whole dict) | | stays `parameters` | |

So a namespace prefixes **node names, datasets and `params:` keys** (`params:opts` →
`params:ds1.opts`, i.e. YAML `ds1: {opts: ...}`). The only exceptions are names listed in
`inputs`/`outputs`/`parameters` and the `parameters` input. `tags=` adds to node tags and never
replaces them.

Mapping errors (verified on 1.7.0):

```text
PipelineError: Failed to map datasets and/or parameters onto the nodes provided: nope does not exist in the pipeline.
PipelineError: ... params:nope does not exist in the pipeline. - did you mean one of these instead: params:opts
PipelineError: Inputs must not be outputs from another node in the same pipeline        # inputs={"mid"}
PipelineError: All outputs must be generated by some node within the pipeline           # outputs={"raw": ...}
```

### Recipe: the same pipeline twice with different parameters (verified on 1.7.0)

```python
# src/<pkg>/pipelines/toy_ns/__init__.py   <- own folder, so find_pipelines() and --pipelines see it
from kedro.pipeline import Pipeline
from ..toy import create_pipeline as create_toy

def create_pipeline(**kwargs) -> Pipeline:
    toy = create_toy()
    return (
        Pipeline(toy, namespace="a", parameters={"params:report"})   # shared param stays un-prefixed
        + Pipeline(toy, namespace="b", parameters={"params:report"})
    )
```

```yaml
# conf/base/parameters_toy_ns.yml   -> params:a.toy / params:b.toy
a:
  toy: {n: 2, scale: 1.0}
b:
  toy: {n: 3, scale: 10.0}
```

Behaviour: nodes `a.make_numbers` and `b.make_numbers` run with their own parameters,
`--namespaces b` runs only the `b` branch, and `--params b.toy.n=...` overrides one branch.
Without a namespace the combination fails with the duplicate-name `ValueError`.

**Catalog trap:** the namespaced datasets are now `a.toy_numbers`, and so on. The catalog entry
`toy_numbers` no longer matches them, so they silently became `MemoryDataset` and nothing was
written to disk (verified on 1.7.0). Add explicit entries or a factory pattern
(`"{ns}.toy_numbers"`), or list the dataset in `inputs`/`outputs` so it keeps its name.

## `kedro pipeline create` / `delete`

`kedro pipeline create toy` creates (verified on 1.7.0):

```text
conf/base/parameters_toy.yml                      # comments only
src/<pkg>/pipelines/toy/__init__.py               # exports create_pipeline
src/<pkg>/pipelines/toy/nodes.py                  # docstring only
src/<pkg>/pipelines/toy/pipeline.py               # def create_pipeline(**kwargs) -> Pipeline: return Pipeline([])
tests/pipelines/toy/__init__.py
tests/pipelines/toy/test_pipeline.py              # docstring only
```

Options: `--skip-config` (no parameters file), `-e/--env` (config env, default `base`),
`-t/--template DIR` (cookiecutter; `<root>/templates/pipeline` is picked up automatically).
Since 1.5, Python keywords are rejected as names.

`kedro pipeline delete toy -y` removes `conf/base/parameters_toy.yml` (if it exists),
`src/<pkg>/pipelines/toy` and `tests/pipelines/toy`; `-e` picks the config env. Without `-y` it
prompts `[y/N]`, and answering N gives `KedroCliError: Deletion aborted!`. It does
**not** edit `pipeline_registry.py`; it only prints a reminder (verified on 1.7.0).

Running the fresh, empty scaffold fails with
`ValueError: Pipeline contains no nodes after applying all provided filters. Please ensure that at least one pipeline with nodes has been defined.`
(verified on 1.7.0).

## Pipeline registry

`src/<pkg>/pipeline_registry.py` must expose `register_pipelines() -> dict[str, Pipeline]`.
This is the 1.7.0 template:

```python
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

def register_pipelines() -> dict[str, Pipeline]:
    pipelines = find_pipelines(raise_errors=True)          # template default since 1.2
    pipelines["__default__"] = sum(pipelines.values())     # what plain `kedro run` runs
    return pipelines
```

- `find_pipelines()` imports every `src/<pkg>/pipelines/<name>/` package, calls
  `create_pipeline()` and keys the result by folder name. With `raise_errors=False` a broken
  pipeline only triggers a warning and is skipped. With `True` the first error aborts.
- `find_pipelines(pipelines_to_find=["data_science"])` (1.3+) loads only those pipelines.
  `None`, or a list that contains `"__default__"`, loads everything.
- Pipelines added to the dict **after** building `__default__` are not part of the default
  pipeline. Example: `pipelines["x"] = Pipeline(pipelines["dp"], tags="x")` means
  `kedro run --tags x` finds nothing; use `--pipelines x --tags x`.

### Selective loading breaks hand-registered pipelines

Since 1.5, `kedro run --pipelines NAME` (and `registry describe NAME`) tells `find_pipelines`
to import **only** `src/<pkg>/pipelines/NAME/`. The CLI filter overrides `pipelines_to_find`.
A pipeline that is only assembled inside `register_pipelines()`, with no folder of its own,
therefore fails (verified on 1.7.0):

```text
$ kedro run --pipelines toy_ns          # toy_ns built in register_pipelines() from pipelines["toy"]
ImportError: An error occurred while importing the 'demo_project.pipelines.toy_ns' module.
```

`kedro registry list` still shows it, because it loads everything. Fix: give every runnable
pipeline its own folder that exposes `create_pipeline()` (recipe above), or run it inside
`__default__` and select it with `--namespaces`/`--tags`. The same `ImportError` is what a
**typo** in `--pipelines` produces under `raise_errors=True`: there is no suggestion. With
`raise_errors=False` you get
`ValueError: Failed to find the pipeline named 'toyy'. It needs to be generated and returned by the 'register_pipelines' function. Did you mean one of these instead?` followed by the candidates (verified on 1.7.0).

## Slicing

CLI flags combine as an **intersection**. `Pipeline.filter(...)` applies each filter to the full
pipeline and intersects the results, so flag order does not matter. An empty result raises
`ValueError: Pipeline contains no nodes after applying all provided filters...`.

| CLI (`kedro run ...`) | Python | Selects |
|---|---|---|
| `--nodes a,b` / `-n` | `p.only_nodes("a", "b")` | exactly these nodes |
| `--from-nodes a` | `p.from_nodes("a")` | `a` and everything downstream |
| `--to-nodes z` | `p.to_nodes("z")` | `z` and everything upstream |
| `--from-inputs ds` | `p.from_inputs("ds")` | nodes downstream of dataset `ds` |
| `--to-outputs ds` | `p.to_outputs("ds")` | nodes needed to produce `ds` |
| `--tags t1,t2` / `-t` (repeatable) | `p.only_nodes_with_tags("t1", "t2")` | nodes with **any** tag (OR) |
| `--namespaces ns1,ns2` / `-ns` | `p.only_nodes_with_namespaces(["ns1"])` | namespace `ns1` **and its children** (`ns1.sub`), exact segment match |
| combination | `p.filter(tags=..., from_nodes=..., node_names=..., from_inputs=..., to_outputs=..., node_namespaces=...)` | intersection |

Verified on 1.7.0 with nodes `len_node → mean_node(tags mean) / mean_sos(tags mean, variance) → variance_node(tags variance)`:
`only_nodes_with_tags("mean", "variance")` returns all three tagged nodes (OR). **The
`build/slice_a_pipeline` doc claims AND; the docstring and the behaviour are OR.** For AND,
intersect: `p.only_nodes_with_tags("a") & p.only_nodes_with_tags("b")`.

Namespaces: `--namespaces data` matches `data.x` and `data.sub.x` but not `data_2.x`, and
`--namespaces dat` fails (exact match since 1.0, verified on 1.7.0).

Slicing errors (verified on 1.7.0):

```text
ValueError: Pipeline does not contain nodes named ['totl'].                    # --nodes / --from-nodes / --to-nodes
ValueError: Pipeline does not contain datasets named ['nope']                  # --from-inputs / --to-outputs
ValueError: Pipeline does not contain nodes with the following namespaces: ['nope']
ValueError: Pipeline input(s) {'toy_doubled'} not found in the DataCatalog...  # slice starts after a MemoryDataset
```

The last error is the classic slicing trap. If a slice cuts off the producer of an in-memory
dataset, nothing can provide it. Persist intermediates you intend to slice at (catalog entry),
or include the producer in the slice.

## Typed parameter validation (1.3+)

Annotate a `params:` input with a Pydantic v2 model or a dataclass. Before any node runs, Kedro
converts the dict and passes the instance to the function. Untyped, primitive-typed and
multi-type-union params are passed through unchanged; `Optional[Model]` is validated.

```python
class ToyParams(BaseModel):          # pydantic (kedro[pydantic] extra)
    n: int
    scale: float = 1.0

@dataclass
class ReportParams:
    label: str

def make_numbers(p: ToyParams) -> list: ...            # Node(make_numbers, "params:toy", ...)
def total(xs: list, rp: ReportParams) -> dict: ...     # Node(total, ["toy_doubled", "params:report"], ...)
```

Behaviour (verified on 1.7.0):

| Case | Result |
|---|---|
| valid YAML | node receives `ToyParams(n=4, scale=1.5)`, not a dict |
| `--params toy.n=abc` | fails **before any node runs**: `ParameterValidationError: Parameter validation failed:\n- Parameter 'toy': Failed to instantiate ToyParams for parameter 'toy': 1 validation error for ToyParams\nn\n  Input should be a valid integer...` |
| dataclass + unknown key (`report.extra=1`) | `... Failed to instantiate ReportParams for parameter 'report': ReportParams.__init__() got an unexpected keyword argument 'extra'` |
| dataclass + wrong type (`report.label=7`) | **accepted**: dataclasses only check that the fields exist |
| namespaced param (`params:b.toy`) | validated as `Parameter 'b.toy'` (fixed in 1.4) |
| `--pipelines toy --nodes total` with a bad `toy` param | **still fails**: the scope is the whole selected pipeline, not the slice |
| `--pipelines toy` with a bad param used only by another pipeline | passes: since 1.4 the scope is the pipelines named in `--pipelines` |
| plain `kedro run` | scope is `__default__`, usually every pipeline |

The `configure/how_to_use_parameters_and_credentials` page still says validation always covers
all pipelines. That is outdated for runs with `--pipelines` (1.4 release notes, verified).
