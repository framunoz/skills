# Cheatsheet: decisions

## Where does this go?

| Thing | Place |
|---|---|
| Dataset definitions | `conf/base/catalog*.yml` (per-pipeline files allowed: `catalog_ingest.yml`) |
| Tunable values | `conf/base/parameters_<pipeline>.yml` |
| Personal overrides | `conf/local/` (git-ignored) |
| Secrets | `conf/local/credentials.yml` (or `conf/<env>/credentials.yml`), `${oc.env:…}` inside |
| Values shared by catalog and parameters | `conf/base/globals.yml` → `${globals:…}` |
| Values supplied at run time | `${runtime_params:key, default}` in YAML + `--params key=value` |
| Deployment-specific config | `conf/<env>/` + `--env <env>` (local not loaded) |
| Transformation logic | pure functions in `pipelines/<name>/nodes.py` |
| Wiring | `pipelines/<name>/pipeline.py` → `create_pipeline()` |
| Cross-cutting behaviour (timing, tracking, validation of everything) | hooks in `settings.HOOKS` |
| Loader/merge/session customisation | `settings.py` |

## Parameter or constant?

| Parameter (`conf/base/parameters_<pipeline>.yml`) | Constant (in `nodes.py` / `constants.py`) |
|---|---|
| Values you tune or experiment with: thresholds, learning rates, depths, seeds | Schema facts: column names, dtypes, expected categories |
| Business rules that change: cutoffs, date ranges, station lists | Mathematical/physical constants |
| Processing knobs: window sizes, sampling ratios, batch sizes | File-format details, regexes tied to the data format |
| Anything that differs per environment or namespace | Display strings |

Rule of thumb: if changing it should not require a code review, make it a parameter (and type it
with Pydantic); if changing it means the data contract changed, keep it in code.

## Which dataset type?

| Data | Type (extra `kedro-datasets[...]`) |
|---|---|
| CSV in/out with pandas | `pandas.CSVDataset` (`pandas-csvdataset`) |
| Tabular intermediates | `pandas.ParquetDataset` / `polars.EagerPolarsDataset` |
| Excel input | `pandas.ExcelDataset` |
| NetCDF / xarray | `kedro_datasets_experimental.netcdf.NetCDFDataset` (full path, `netcdf-netcdfdataset`) |
| Model object | `pickle.PickleDataset` (or `joblib` backend), versioned |
| Metrics / small dicts | `json.JSONDataset` |
| Figures | `matplotlib.MatplotlibDataset`, `plotly.JSONDataset` / `plotly.PlotlyDataset` |
| SQL tables | `pandas.SQLTableDataset` / `pandas.SQLQueryDataset` (credentials: `con`) |
| Many files in a folder | `partitions.PartitionedDataset` (only new ones: `IncrementalDataset`) |
| Throwaway intermediate | nothing — `MemoryDataset` (lost after the run) |

Always confirm with `scripts/check_dataset.py <type>`.

## Which runner?

| Situation | Runner |
|---|---|
| Default, debugging, hooks everywhere | `SequentialRunner` |
| I/O-bound nodes (cloud reads, APIs), Spark | `ThreadRunner` (`--runner ThreadRunner --runner-params max_workers=4`) |
| CPU-bound independent nodes, picklable functions/datasets | `ParallelRunner` (no lambdas; node hooks don't run in workers) |

## Which merge strategy?

| Want | `merge_strategy["parameters"]` |
|---|---|
| `local`/`--params` override single nested keys | `soft` (recommended for data science) |
| An env replaces whole parameter groups | `destructive` (default) |

## Re-running

| Need | Flag |
|---|---|
| Pipelines by name | `--pipelines a,b` (`--pipeline` deprecated in 1.7) |
| One namespace | `--namespaces x` (exact match; several allowed) |
| Nodes by tag | `--tags t1,t2` (OR) |
| From / to | `--from-nodes`, `--to-nodes`, `--from-inputs`, `--to-outputs` |
| Skip existing outputs | `--only-missing-outputs` |
| Different config set | `--env`, `--conf-source` |
| Reproducible run definition | `-c run.yml` |

## Which verification?

| Question | Tool |
|---|---|
| Right interpreter/versions? stale 0.19 code? secrets in base? | `scripts/kedro_preflight.py` |
| Does this dataset type exist, which args/extra? | `scripts/check_dataset.py` |
| What's undeclared / unpersisted / mis-parametrised? | `scripts/kedro_snapshot.py` |
| How does a name resolve against factories? | `kedro catalog resolve-patterns`, `list-patterns`, `describe-datasets` |
| What pipelines exist? | `kedro registry list`, `kedro registry describe <name>` |
| Does it actually work? | `uv run kedro run --pipelines <name>` on small data; `uv run pytest` |
| What does it look like? | `uv run kedro viz run` |
