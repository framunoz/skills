# Deployment and Kedro-Viz

A Kedro deployment has three separate parts: **code** (a wheel), **config** (a tarball or
directory passed at run time), and **data** (wherever the catalog points). Orchestrators run
the same package and differ only in how they split nodes into tasks. Verified on 1.7.0 and
kedro-viz 12.5.0 unless marked otherwise.

## `kedro package`

There are no options except `-h`. Run it from the project root:

```
dist/
├── <package>-<version>-py3-none-any.whl   # src/<package>/** only: no conf/, no data/
└── conf-<package>.tar.gz                  # conf/ minus local/*.yml
```

- The tarball is built with `tar --exclude=local/*.yml -czf dist/conf-<pkg>.tar.gz conf`. So
  `conf/local/credentials.yml` is excluded, but `conf/local/` and its `.gitkeep` are kept. Files
  like `conf/base/*.yml` and `conf/README.md` are included.
- The wheel carries the project's entry points: a `console_scripts` entry
  `<project-name> = <pkg>.__main__:main`, plus any `kedro.*` plugin entry points declared in
  `pyproject.toml`.
- `setuptools` leaves a `build/` dir behind, and `kedro viz build` writes to the same `build/`
  (see below). Both are git-ignored by the template.
- The version comes from `<pkg>.__version__`, through
  `[tool.setuptools.dynamic] version = {attr = "<pkg>.__version__"}`.

### Running the packaged project

```bash
uv venv && uv pip install dist/<pkg>-0.1-py3-none-any.whl   # pulls kedro + deps; no project dir needed
python -m <pkg> --conf-source=conf-<pkg>.tar.gz --pipelines=data_processing
<project-name> --conf-source=/abs/path/conf --env=prod       # console script, same CLI
```

```python
from <pkg>.__main__ import main
main(["--pipelines", "__default__"])   # in a notebook/Databricks main() returns the session.run() output
```

- `python -m <pkg> --help` shows the `kedro run` options (`--pipelines`, `-n/--nodes`,
  `-t/--tags`, `-ns/--namespaces`, `-e/--env`, `--params`, `--conf-source`, `-r/--runner`,
  `--runner-params`, `--only-missing-outputs`, `-lv/--load-versions`, `--from-*/--to-*`, `--async`).
- `--conf-source` accepts a directory, a `.tar.gz`, a `.zip` (opened by OmegaConfigLoader
  through fsspec, after it guesses the mimetype), or a remote/cloud URL (`s3://`, `https://`,
  read from source). Without it, Kedro looks for `./conf/base` in the **cwd** and fails with:
  `MissingConfigException: Given configuration path either does not exist or is not a valid directory: <cwd>/conf/base`.
- `default_run_env: local` is still active in the packaged `settings.py`. A conf dir without
  `local/` fails with
  `MissingConfigException: ... is not a valid directory: <conf>/local`. Fix it with an empty
  `local/` directory or `--env=base` (both verified).
- Relative catalog paths (`data/01_raw/...`) resolve against the **cwd**. A missing file shows
  up as `DatasetError: companies: Failed while loading data from dataset ...` wrapping
  `FileNotFoundError`. In production, point the catalog at object storage with a prod env
  (`conf/prod/catalog.yml`), or ship `data/`.
- Hooks in `settings.py` are inside the wheel, so they run in the deployed package (verified).

## Node grouping for orchestrators

Mapping one node to one task means many containers and many reloads of intermediate data. Group
nodes instead:

| Unit | CLI selection | Fit |
|---|---|---|
| Registered pipeline | `--pipelines=a,b` | Coarse; you already have the split |
| Tag | `--tags=x` | Ad-hoc subsets; tags aren't hierarchical and nodes can sit in several |
| **Pipeline-level namespace** | `--namespaces=ns1,ns2` (1.0+, several allowed) | **Recommended deployment unit**: one namespace = one task/job |

`Pipeline.group_nodes_by(group_by: str | None = "namespace") -> list[GroupedNodes]` (1.0+,
replaces `grouped_nodes_by_namespace`):

```python
from kedro.pipeline import Pipeline, Node
p = Pipeline(base, namespace="ns1", inputs={"a"}) + Pipeline([Node(f, "ns1.c", "d", name="n3")])
p.group_nodes_by("namespace")
# [GroupedNodes(name='ns1', type='namespace', nodes=['ns1.n1','ns1.n2'], dependencies=[]),
#  GroupedNodes(name='n3',  type='nodes',     nodes=['n3'],               dependencies=['ns1'])]
p.group_nodes_by(None)   # or "none": one group per node; dependencies are node names
p.group_nodes_by("tags") # ValueError: Unsupported group_by strategy: tags
```

- `GroupedNodes(name, type, nodes: list[str], dependencies: list[str])`. Nodes without a
  namespace become singleton groups of type `"nodes"`. Grouping uses the **top-level**
  namespace.
- Each task runs `python -m <pkg> --namespaces=<group.name>` (or `--nodes=...` for
  `type == "nodes"`). Datasets passed **between** groups must be persisted (not `MemoryDataset`),
  and on shared or object storage, not local disk.
- A namespace set at the pipeline level prefixes inputs, outputs and params with `ns.`. Exclude
  names with `inputs=`, `outputs=` or `parameters=`. A namespace set at the node level is only
  visual (kedro-viz collapsing) and does not make a deployment unit.
- `kedro airflow create --group-by namespace` follows the same model. The AWS Step Functions and
  AWS Batch guides use `group_nodes_by("namespace")`.
- `kedro.inspection.validate_deployment_grouping` is **not in 1.7.0** (upcoming release only).
- The `deploy/nodes_grouping` page still says "Kedro allows executing one namespace at a time".
  That is stale: `--namespaces` accepts several since 1.0.

## Platform guides (`deploy/...`)

| Platform | Doc path | Mechanism (summarised from guide/plugin, not exercised) |
|---|---|---|
| Overview | `deploy` | Strategy overview |
| Single machine | `deploy/single_machine` | Container, package, or git clone on one VM |
| Distributed | `deploy/distributed` | Containerise, one node/group per container |
| Apache Airflow | `deploy/supported-platforms/airflow` | kedro-airflow DAG generation |
| Amazon SageMaker | `deploy/supported-platforms/amazon_sagemaker` | kedro-sagemaker |
| Amazon EMR Serverless | `deploy/supported-platforms/amazon_emr_serverless` | Spark job, custom image |
| AWS Step Functions | `deploy/supported-platforms/aws_step_functions` | Lambda per namespace |
| AWS Batch | `deploy/supported-platforms/aws_batch` | Custom `AWSBatchRunner`, job per namespace |
| Azure ML | `deploy/supported-platforms/azure` | kedro-azureml |
| Dagster | `deploy/supported-platforms/dagster` | kedro-dagster |
| Dask | `deploy/supported-platforms/dask` | Custom `DaskRunner` |
| Databricks | `deploy/supported-platforms/databricks` | kedro-databricks / notebooks |
| Kubeflow Pipelines | `deploy/supported-platforms/kubeflow` | kedro-kubeflow |
| Prefect | `deploy/supported-platforms/prefect` | Guide-only (no maintained plugin) |
| Vertex AI | `deploy/supported-platforms/vertexai` | kedro-vertexai |
| Argo Workflows | `deploy/supported-platforms/argo` | Guide-only |

Also: `kedro server start` (1.5+), an HTTP server with `/run`, `/health` and `/snapshot` built on
`KedroServiceSession` (docs only, not exercised here).

## Kedro-Viz

`kedro viz` with no arguments runs `kedro viz run`: the group sets `default="run"` and
`default_if_no_args=True`. Subcommands: `run`, `build`, `deploy`.

### `kedro viz run` (verified `--help`, server started and `/api/main` served)

| Option | Default | Notes |
|---|---|---|
| `--host` | `localhost` | Use `0.0.0.0` in containers |
| `--port` | `4141` | |
| `--browser/--no-browser` | browser | Opens a browser only when the host is localhost |
| `-a, --autoreload` | off | Restarts on `.py`/`.yml` changes |
| `--include-hooks` | off | **Without it, project hooks don't run** (verified) |
| `-p, --pipeline` | `__default__` | |
| `-e, --env` | `local` | |
| `--params` | | Same syntax as `kedro run --params` |
| `--load-file` / `--save-file` | | Save or restore the viz JSON (useful when the env lacks deps) |
| `--lite` | off | Experimental: renders without the project's dependencies; unresolvable datasets show as `UnavailableDataset` and **layers are not shown** |

### `kedro viz build` / `deploy`

- `kedro viz build [--include-hooks] [--include-previews]` writes a static site into
  **`build/`** (`index.html` plus `api/main`, `api/nodes/<id>`, `api/pipelines/...`). Serve it
  with any static host. Previews are **off by default** for build/deploy, so pass
  `--include-previews` (verified).
- `kedro viz deploy --platform {aws,azure,gcp} --endpoint <url> --bucket-name <b> [--include-hooks] [--include-previews]`
  uploads the build to a bucket.

### Catalog metadata for Viz

```yaml
companies:
  type: pandas.CSVDataset
  filepath: data/01_raw/companies.csv
  metadata:
    kedro-viz:
      layer: raw                 # → node "layer": "raw"; groups the flowchart into horizontal bands
      preview_args:
        nrows: 3                 # TablePreview rows (default 5)
      # preview: false           # disable preview for this dataset
```

Verified in `build/api/main`: `layers: ['raw']`, and the companies node has
`"layer": "raw"`. Its preview has 3 rows (`preview_type: TablePreview`). The top-level
`layer:` key on a dataset was removed in 0.19, so it must sit under `metadata.kedro-viz`.
Preview types are TablePreview (pandas CSV/Excel per docs), PlotlyPreview, ImagePreview
(matplotlib) and JSONPreview. Custom datasets get a preview by implementing `preview()`.

### Viz runtime artefacts

kedro-viz registers `kedro.hooks` (`kedro-dataset-stats`, `pipeline-run-hook`). Every
`kedro run` writes `.viz/stats.json` and `.viz/kedro_pipeline_events.json` (the latter feeds the
Workflow view, and is written for sequential runs only). The template git-ignores `.viz`. Turn
them off with `DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)`. `%run_viz` in a notebook comes from
kedro-viz's `kedro.line_magic` entry point.

## Telemetry (docs: `about/telemetry`)

The `kedro-telemetry` plugin is a hard dependency of kedro and kedro-viz. It sends anonymised
CLI usage. To opt out, use any of:

| Method | Scope |
|---|---|
| `KEDRO_DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` (any value) | Whole environment. Overrides `.telemetry` |
| `.telemetry` file in project root with `consent: false` | That project (the template git-ignores it) |
| `kedro new --telemetry=no` | Writes that file. The `kedro new` call itself still reports unless the env var is set |
| Uninstall `kedro-telemetry` | Last resort: breaks `pip check` |

Without explicit consent, the CLI prompts or prints a notice on first use. In CI, containers and
agent sessions, always export `KEDRO_DISABLE_TELEMETRY=1`. Per the docs, the plugin stores an anonymous
user UUID in an OS config dir (`telemetry.toml`) and a project UUID in `pyproject.toml`.
This section is docs only; nothing was sent while testing.
