# Data Catalog: entries, datasets, factories, versioning, validation, API

Kedro 1.7.0 + kedro-datasets 9.6.0. "(verified on 1.7.0)" = run in a scratch spaceflights project.

The catalog maps every node input/output name to a dataset object (load/save logic + location).
Config lives in `conf/<env>/catalog*.yml` (also `catalog/**/*.yml`); `conf/local` overrides
`conf/base` per **top-level key** (whole entry replaced, not deep-merged).

## Entry anatomy

```yaml
companies:                          # dataset name = node input/output string
  type: pandas.CSVDataset           # required
  filepath: s3://bucket/raw/companies.csv
  load_args: {sep: ",", dtype: {id: str}}     # -> pd.read_csv(**load_args)
  save_args: {index: false}                   # -> df.to_csv(**save_args)
  fs_args:                                    # -> fsspec filesystem constructor
    project: my-gcp-project
    open_args_load: {mode: "r", encoding: utf-8}   # -> fs.open() on load
  credentials: dev_s3                         # name of a block in credentials.yml
  metadata:                                   # free-form; ignored by Kedro itself
    kedro-viz:
      layer: raw                              # Kedro-Viz layer grouping
  versioned: true
  validator: my_project.schemas.CompaniesSchema   # 1.6+, see Validation
```

| Key | What it is |
|---|---|
| `type` | Short `pandas.CSVDataset` or full `kedro_datasets.pandas.CSVDataset`, or any dotted path to an `AbstractDataset` subclass (`my_project.datasets.ImageDataset`). Resolution tries `kedro.io.`, then `kedro_datasets.`, then the string as-is — **not** `kedro_datasets_experimental.` (verified on 1.7.0) |
| `filepath` | fsspec URL. No protocol = local, relative to project root. `s3://` (s3fs), `gcs://`/`gs://` (gcsfs), `abfs://` (adlfs), `hdfs://`, `http(s)://` (no versioning), `sftp://`… Protocol libs are separate installs |
| `load_args` / `save_args` | Passed verbatim to the underlying library call. Defaults per dataset: `DEFAULT_LOAD_ARGS` / `DEFAULT_SAVE_ARGS` (e.g. `pandas.CSVDataset` saves with `index: False`) |
| `fs_args` | Top level → filesystem class; `open_args_load` / `open_args_save` → `fs.open()` |
| `credentials` | String key into `conf/<env>/credentials.yml`; the block's contents become the `credentials=` constructor arg. For fsspec datasets that is fs kwargs (`key`/`secret`, `client_kwargs`, `token`…); for SQL datasets `{con: <sqlalchemy URL>}` |
| `metadata` | Any dict; Kedro passes it to the constructor and ignores it. `metadata: kedro-viz: layer:` is how layers are declared |
| `versioned` | `true` → timestamped subfolders, see Versioning |
| `validator` | 1.6+; stripped by the catalog before the constructor |

Every other key must be a constructor argument of that dataset class. Unknown keys raise
**when the dataset is first materialised** (catalog is lazy), not at startup — a broken entry
that no node of the selected pipeline uses lets `kedro run` complete (verified on 1.7.0):

```
DatasetError:
CSVDataset.__init__() got an unexpected keyword argument 'load_arg'. Did you mean 'load_args'?.
Dataset 'bad_arg' must only contain arguments valid for the constructor of 'kedro_datasets.pandas.csv_dataset.CSVDataset'.
```

A missing `type`, or a top-level key whose value is not a dict, fails **eagerly** at session
start and blocks every command (verified on 1.7.0):

```
DatasetError: An exception occurred when parsing config for dataset 'no_type':
'type' is missing from dataset catalog configuration.
Hint: If this catalog entry is intended for variable interpolation, make sure that the top level key is preceded by an underscore.

DatasetError: Catalog entry 'base_dir' is not a valid dataset configuration.
Hint: If this catalog entry is intended for variable interpolation, make sure that the key is preceded by an underscore.
```

### `_`-prefixed keys: templates and variables

Top-level keys starting with `_` are dropped by the config loader → never datasets. Use them for
YAML anchors and OmegaConf interpolation (verified on 1.7.0):

```yaml
_csv: &csv
  type: pandas.CSVDataset
  load_args: {sep: ","}
_raw: data/01_raw

companies:
  <<: *csv                       # merge; local keys override whole sub-dicts (load_args replaced, not merged)
  filepath: ${_raw}/companies.csv
```

`catalog["_csv"]` → `DatasetNotFoundError`. Without the `_`, an anchor entry that has a `type`
silently becomes a dataset (fails only when used: `missing 1 required keyword-only argument: 'filepath'`).
The `_` filtering is done by `OmegaConfigLoader`; `DataCatalog.from_config({...})` in plain
Python does **not** filter (`_tmpl` showed up in `catalog.keys()`, verified on 1.7.0).

### Environment variables

`${oc.env:VAR}` is enabled **only in credentials** files. In `catalog.yml` it fails at session
start (verified on 1.7.0):

```
omegaconf.errors.UnsupportedInterpolationType: Unsupported interpolation type oc.env
    full_key: env_test.filepath
```

Fix: put the secret/endpoint in `credentials.yml` (`${oc.env:...}` works there), use
`${globals:...}` / `${runtime_params:...}`, or opt in for all config in `settings.py`
(docs discourage it):

```python
from omegaconf.resolvers import oc
CONFIG_LOADER_ARGS = {"custom_resolvers": {"oc.env": oc.env}}
```

## kedro-datasets

- Datasets left core Kedro in 0.19; `kedro.extras.datasets` is gone
  (`ModuleNotFoundError: No module named 'kedro.extras'`). Install `kedro-datasets`.
- Since kedro-datasets 2.0 the suffix is `Dataset` (lower-case s). `CSVDataSet` fails (see Gotchas).
- Install per dataset with extras named `<group>-<lowercased class>`:
  `uv add "kedro-datasets[pandas-csvdataset,pandas-parquetdataset]"`, or a whole group:
  `kedro-datasets[pandas]`, `[polars]`, `[plotly]`. Protocol libs (s3fs, gcsfs, adlfs) are
  separate (`[s3fs-base]` exists for s3fs).
- Experimental datasets ship **inside the same wheel** as the `kedro_datasets_experimental`
  package; extras like `kedro-datasets[netcdf]`. They need the **full** type path:
  `type: kedro_datasets_experimental.netcdf.NetCDFDataset` (`netcdf.NetCDFDataset` →
  `No module named 'netcdf'`, verified on 1.7.0).

Constructor args for any dataset (markdown pages, all return 200):

```
https://docs.kedro.org/projects/kedro-datasets/en/stable/api/kedro_datasets/<group>.<Class>/index.md
https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-9.6.0/api/kedro_datasets/pandas.CSVDataset/index.md   # pinned version
https://docs.kedro.org/projects/kedro-datasets/en/stable/api/kedro_datasets_experimental/netcdf.NetCDFDataset/index.md
```

Or locally: `uv run python -c "import inspect, kedro_datasets.pandas as m; print(inspect.signature(m.CSVDataset))"`.
Index: `https://docs.kedro.org/projects/kedro-datasets/en/stable/llms.txt`.

### Common types for data science (present in 9.6.0)

| Data | `type` |
|---|---|
| Tabular | `pandas.CSVDataset`, `pandas.ParquetDataset`, `pandas.ExcelDataset` (multi-sheet: `load_args: {sheet_name: null}` → dict), `pandas.FeatherDataset`, `pandas.JSONDataset`, `pandas.XMLDataset`, `pandas.HDFDataset`, `pandas.GenericDataset` (any `pd.read_<file_format>`) |
| SQL | `pandas.SQLTableDataset` (`table_name`, `credentials: {con: ...}`), `pandas.SQLQueryDataset` (`sql` or `filepath` to .sql) |
| Polars | `polars.EagerPolarsDataset` / `polars.LazyPolarsDataset` (`file_format: parquet`), `polars.CSVDataset` |
| Python objects | `pickle.PickleDataset` (`backend: pickle` default, `joblib`, or any module with `load`/`dump`), `json.JSONDataset`, `yaml.YAMLDataset`, `text.TextDataset` |
| Plots | `matplotlib.MatplotlibDataset` (**save-only**; figure, or list/dict of figures → folder), `plotly.PlotlyDataset` (builds fig from `plotly_args`), `plotly.JSONDataset`, `plotly.HTMLDataset` |
| Images | `pillow.ImageDataset` |
| Spark / Dask / Ibis | `spark.SparkDataset`, `spark.SparkDatasetV2`, `dask.ParquetDataset`, `ibis.TableDataset` |
| Geo | `geopandas.GenericDataset`; experimental `kedro_datasets_experimental.rioxarray.GeoTIFFDataset` |
| xarray / netCDF | experimental only: `kedro_datasets_experimental.netcdf.NetCDFDataset` |
| Folders of files | `partitions.PartitionedDataset`, `partitions.IncrementalDataset` |
| In-memory / cache | `kedro.io.MemoryDataset` (`MemoryDataset`), `kedro.io.CachedDataset` (`CachedDataset`) |

## Undeclared datasets → MemoryDataset

A name used in a pipeline but matching no entry/pattern becomes a `MemoryDataset` at run time
(runtime pattern `{default}`; `SharedMemoryDataset` under `ParallelRunner`). It lives for that
run only. Outside a run (verified on 1.7.0):

| Call | Result for an undeclared name |
|---|---|
| `"x" in catalog` | `False` |
| `catalog["x"]` | `DatasetNotFoundError: Dataset 'x' not found in the catalog` |
| `catalog.get("x")` | `None` |
| `catalog.get("x", fallback_to_runtime_pattern=True)` | `MemoryDataset()` |
| `catalog.load("x")` | `DatasetError: x: Data for MemoryDataset has not been saved yet.` |

`MemoryDataset(copy_mode=...)`: `"deepcopy"`, `"copy"`, `"assign"`. Inferred when unset (`_infer_copy_mode`): pandas DataFrame / numpy array
→ `copy`; any other class named `DataFrame` (polars, Spark) or an Ibis table → `assign`; else `deepcopy`. So a node never receives the same DataFrame
object another node returned (verified: `load() is df` → `False`; with `assign` → `True`).
Declare `type: MemoryDataset` + `copy_mode: assign` for objects that can't be copied (DB
connections, some models) or to save memory.

`CachedDataset` wraps a dataset and keeps the last loaded/saved value in memory:

```yaml
model_input_table:
  type: CachedDataset
  dataset:
    type: pandas.ParquetDataset
    filepath: data/03_primary/model_input_table.parquet
```

## Dataset factories

Pattern keys with `{placeholders}` (Python `parse` syntax, a reversed f-string) generate entries on
demand. Quote the key. Every placeholder used in the body must appear in the key.

```yaml
"{name}@csv":
  type: pandas.CSVDataset
  filepath: data/01_raw/{name}.csv

"{namespace}.{name}_model":         # several placeholders
  type: pickle.PickleDataset
  filepath: data/06_models/{namespace}/{name}.pkl
  versioned: true
  metadata: {kedro-viz: {layer: "{namespace}"}}

"{default_ds}":                     # user catch-all: replaces MemoryDataset for everything unmatched
  type: pickle.PickleDataset
  filepath: data/09_tmp/{default_ds}.pkl
```

Resolution order: explicit entry → dataset patterns (ranked) → the one user catch-all →
runtime `{default}` (MemoryDataset). Using the catch-all logs a WARNING per dataset:
`Config from the dataset pattern '{default_ds}' in the catalog will be used to override the default dataset creation for 'X_test'`.

**Ranking is by specificity, never by file position** (verified on 1.7.0: patterns written in
reverse order came back sorted). Sort key, from `CatalogConfigResolver._sort_patterns`:

1. More literal characters (pattern length outside `{}`) first.
2. Tie → more placeholders first.
3. Tie → plain string sort of the pattern (`z{x}` beats `{x}z`, since `z` < `{` in ASCII).

```
$ kedro catalog list-patterns --env t2        # observed order
'{x}_data#csv'  '{ns}.{x}#csv'  '{a}{b}_raw'  '{a}_raw'  '{x}#csv'  '{x}.{y}'  'z{x}'  '{x}z'  '{anything}'  '{default}'
```

| Name | Matched (verified) | Why |
|---|---|---|
| `factory_data#csv` | `{x}_data#csv` | 9 literals vs 4 |
| `pre.shuttles#csv` | `{ns}.{x}#csv` | 5 literals vs `{x}#csv` 4 |
| `foo_raw` | `{a}{b}_raw` (a=`f`, b=`oo`) | same literals as `{a}_raw`, more placeholders |
| `zzz` | `z{x}` | tie → string sort |

Any pattern with **zero literal characters** is a catch-all — `{a}{b}` counts. More than one →
session start fails: `DatasetError: Multiple catch-all patterns found in the catalog: {b}{c}, {a}. Only one catch-all pattern is allowed, remove the extras.` (verified on 1.7.0).

Use a distinctive prefix/suffix (`#csv`, `@pq`, `raw_`) so patterns can't swallow unrelated
names. A pattern's `type` must fit **every** object it captures: `"{split}_train"` →
`pandas.ParquetDataset` also caught `y_train` (a Series) and the run died with
`AttributeError: 'Series' object has no attribute 'to_parquet'` → `DatasetError: y_train: Failed while saving data to dataset ...`
(verified on 1.7.0). Catch-alls are safest as `pickle.PickleDataset`. Validators on factory entries are captured when the dataset is first materialised.

## Transcoding

Same file, two dataset classes; the `@suffix` is stripped for dependency resolution only:

```yaml
model_input@spark:
  type: spark.SparkDataset
  filepath: data/03_primary/model_input.parquet
  file_format: parquet
model_input@pandas:
  type: pandas.ParquetDataset
  filepath: data/03_primary/model_input.parquet
```

Node A outputs `model_input@spark`, node B inputs `model_input@pandas` → B runs after A. In the
catalog they are two separate keys (`"model_input" in catalog` → `False`, verified). A node
cannot have `x@a` as input and `x@b` as output (`ValueError: ... A node cannot have the same
inputs and outputs even if they are transcoded`), and two nodes cannot output `x@a`/`x@b`
(`OutputNotUniqueError`) (docs).

## Versioning

`versioned: true` turns `filepath` into a folder: `<filepath>/<YYYY-MM-DDThh.mm.ss.sssZ>/<filename>`
(verified: `cars.csv/2026-10-09T20.15.24.706Z/cars.csv`). Load = latest unless pinned.
Only datasets subclassing `AbstractVersionedDataset` support it; not with `http(s)://`;
not inside `PartitionedDataset`.

```bash
kedro run --load-versions=regressor:2026-10-09T20.15.24.706Z,model_metrics:2026-...   # -lv; comma-separated name:ts
```

```python
ds = catalog["regressor"]
ds.list_versions(full_path=False)   # 1.3+: ['2026-10-09T20.15.24.706Z', ...] newest first
ds.list_versions()                  # default full_path=True → absolute file paths
catalog.load("regressor", version="2026-10-09T20.15.24.706Z")
DataCatalog.from_config(cfg, load_versions={"regressor": "..."})
```

A pinned version that doesn't exist fails at load with the full path:
`[Errno 2] No such file or directory: '.../data/06_models/regressor.pickle/2001-01-01T00.00.00.000Z/regressor.pickle'`
(verified on 1.7.0). A name the catalog can't resolve fails before any node:
`DatasetNotFoundError: 'load_versions' keys [nonexistent_ds] are not found in the catalog.`
(names resolved via a user catch-all are accepted since 1.7.0). Each `kedro run` writes a new version folder; nothing is pruned.

A catalog has **one save version** (the run timestamp): saving the same versioned dataset twice
through one catalog raises `Save path '.../<ts>/cars.csv' ... must not exist if versioning is enabled.`
(verified on 1.7.0). Fine in `kedro run` (one save per dataset); in notebooks re-create the
catalog (`%reload_kedro`) or use the dataset object with `Version(None, None)`.

## PartitionedDataset and IncrementalDataset

```yaml
daily_logs:
  type: partitions.PartitionedDataset
  path: s3://bucket/logs/            # folder; any fsspec protocol
  dataset:                          # shorthand `dataset: pandas.CSVDataset` also valid
    type: pandas.CSVDataset
    load_args: {parse_dates: [ts]}
  filename_suffix: ".csv"           # filters files and is stripped from partition IDs
  credentials: dev_s3               # top-level creds → filesystem (+ dataset unless it sets its own)
  # save_lazily: true (default)
```

- **Load** returns `dict[partition_id, callable]` — nothing read until you call it
  (verified: values are bound `load` methods). IDs are paths relative to `path`, suffix removed
  (`sub/p2`). Empty folder → `DatasetError: e: No partitions found in 'nope'`.
- **Save** a dict `{partition_id: data_or_callable}`; callables are evaluated at write time
  (lazy saving). Subfolders in IDs are created (verified: `{"p1": df, "sub/p2": lambda: df}` →
  `p1.csv`, `sub/p2.csv`). Beware late binding when building lambdas in a loop
  (`lambda d=d: d`). Existing partitions are overwritten.
- Load result is cached per run; call `release()` to rescan.
- Inner `dataset` must not set `versioned` or `credentials` (→ `DatasetError`); its `filepath`
  is overridden with a warning.

```python
def concat(parts: dict[str, Callable[[], pd.DataFrame]]) -> pd.DataFrame:
    return pd.concat([load() for _, load in sorted(parts.items())], ignore_index=True)
```

`IncrementalDataset` (subclass): loads **eagerly** (values are data, not callables), only
partitions with ID > checkpoint (`comparison_func`, default `operator.gt`), returns `{}` instead of
raising when nothing is new. Checkpoint (`<path>/CHECKPOINT`) advances only when a node declares
`confirms="daily_logs"`; `checkpoint: {force_checkpoint: "2026-01-01"}` to reprocess (docs).

## Validation (1.6+)

```yaml
companies:
  type: pandas.CSVDataset
  filepath: data/01_raw/companies.csv
  validator: my_project.schemas.CompaniesSchema    # pandera DataFrameModel, class with .validate(data), or a function
  # long form:
  # validator:
  #   class: my_project.schemas.CompaniesSchema
  #   on: [load, save]          # default both
  #   severity: error           # or warn
  #   enabled: true
  #   options: {lazy: true}     # constructor kwargs / PanderaValidator kwargs
```

- Pandera: `uv add "kedro[pandera-pandas]"` (or `kedro[pandera-polars]`); schema is plain
  `pandera.pandas.DataFrameModel`.
- Failure → `kedro.validation.DataValidationError` (subclass of `DatasetError`), on load before the
  node runs, on save before writing (verified on 1.7.0):
  ```
  DataValidationError: Validation failed for dataset 'tiny_valid' on load
  (validator: myval.MinRows)
  expected at least 3 rows, got 2
  ```
- Bad import path → `ValidationConfigurationError: Could not import validator 'nope.Nope': No module named 'nope'. ...`
- Class validators must **return the data** (returning `None` feeds `None` to the node); plain
  functions may return `None` = pass-through.
- Off switches: per entry `enabled: false` / `severity: warn`; per project
  `DATASET_VALIDATION = False` in `settings.py`; per run `KEDRO_DATASET_VALIDATION=0 kedro run`
  (overrides everything); in code `DataCatalog.from_config(..., validation_enabled=False)`
  (env var and flag verified on 1.7.0).
- On demand, never raises: `from kedro.validation import validate_dataset, validate_catalog`
  → `ValidationResult(status=passed|failed|skipped|errored)`.
- One validator per dataset.

## DataCatalog in code (1.0 API)

`KedroDataCatalog` became `DataCatalog` in 1.0: dict-like, lazy (entries materialise on first access).

```python
from kedro.io import DataCatalog, MemoryDataset
catalog = DataCatalog.from_config(catalog_cfg, credentials=creds)   # dicts like catalog.yml
catalog = DataCatalog({"cars": CSVDataset(filepath="cars.csv")})    # or instances

df = catalog.load("cars"); catalog.save("cars", df)   # errors are prefixed with the dataset name
catalog.load("cars", version="...")                   # versioned
ds = catalog["cars"]                                  # dataset object; KeyError-like DatasetNotFoundError
catalog.get("x", fallback_to_runtime_pattern=True)    # None if missing (without fallback)
"cars" in catalog                                     # explicit OR matches a pattern/catch-all
catalog.keys(); catalog.values(); catalog.items(); len(catalog); for name in catalog: ...
catalog["feed"] = [1, 2]                              # raw value → wrapped in MemoryDataset
catalog.exists("cars"); catalog.release("cars"); catalog.confirm("parts")
catalog.filter(name_regex="^model_", type_regex="Parquet", by_type=MemoryDataset)
catalog.get_type("x_valid")                           # 'kedro_datasets.pandas.csv_dataset.CSVDataset', no materialising
cfg, creds, load_versions, save_version = catalog.to_config()
catalog.config_resolver.list_patterns(); catalog.config_resolver.resolve_pattern("x")
```

`keys()` lists explicit/materialised entries only, not pattern-matchable names. `"name" in`
checks patterns too.

Removed in 1.0 (all `AttributeError: 'DataCatalog' object has no attribute '...'`, verified):
`list()` → `keys()`/`filter()`; `add_feed_dict()` → `catalog[name] = value`; `add_all()`;
`_get_dataset()` → `catalog[name]` / `get()`; `shallow_copy()`. No `del`/`pop()`.
Saving `None` → `DatasetError: <name>: Saving 'None' to a 'Dataset' is not allowed`.

In `kedro ipython` / `%load_ext kedro.ipython` the catalog is preloaded as `catalog`.

### CLI

`kedro catalog list`/`rank`/`resolve`/`create` were removed in 1.0. Current (verified on 1.7.0):

```bash
kedro catalog describe-datasets -p data_science [--env t9]
kedro catalog list-patterns [--env ...]
kedro catalog resolve-patterns -p data_science [--env ...]
```

```yaml
# describe-datasets: grouped per pipeline by how each name resolves
data_science:
  datasets:                 # explicit entries
    kedro_datasets.pickle.pickle_dataset.PickleDataset: [regressor]
  defaults:                 # user catch-all or MemoryDataset; {} if none
    kedro_datasets.pickle.pickle_dataset.PickleDataset: [X_test, y_test, metrics]
  factories:                # matched a dataset pattern
    kedro_datasets.pandas.parquet_dataset.ParquetDataset: [y_train, X_train]
```

```yaml
# list-patterns: priority order, runtime '{default}' always last
- '{split}_train'
- '{default_ds}'
- '{default}'
```

`resolve-patterns` prints YAML config per dataset: factory/catch-all matches as filled-in config
(`type: pickle.PickleDataset`, absolute `filepath`), explicit entries in expanded form
(full class path, every constructor arg incl. `null`s). It printed **every explicit catalog entry**,
not just those of `-p` — filter the output yourself. `params:` inputs are not listed.
Without `-p`, `__default__` is used. All three print INFO/WARNING log lines before the YAML; parse
from the first unindented key.

## Custom dataset

```python
from kedro.io import AbstractDataset            # AbstractVersionedDataset for versioning

class ImageDataset(AbstractDataset[np.ndarray, np.ndarray]):
    def __init__(self, *, filepath: str, metadata: dict | None = None):
        protocol, path = get_protocol_and_path(filepath)   # from kedro.io.core
        self._protocol, self._filepath = protocol, PurePosixPath(path)
        self._fs = fsspec.filesystem(protocol)
        self.metadata = metadata
    def load(self) -> np.ndarray: ...
    def save(self, data: np.ndarray) -> None: ...
    def _describe(self) -> dict: return {"filepath": self._filepath, "protocol": self._protocol}
```

Required: `load`, `save`, `_describe`. Legacy `_load`/`_save` are still aliased to `load`/`save`
(verified). Missing `_describe` → `Can't instantiate abstract class ... without an implementation
for abstract method '_describe'`. Reference it by dotted path: `type: my_project.datasets.ImageDataset`.
Accept `metadata` if you want `kedro-viz` layers on it. Versioned variant: subclass
`AbstractVersionedDataset`, call `super().__init__(filepath=..., version=version, exists_function=self._fs.exists, glob_function=self._fs.glob)`,
and use `self._get_load_path()` / `self._get_save_path()`.

Docs: `catalog-data/data_catalog`, `catalog-data/how_to_configure_the_data_catalog`,
`catalog-data/kedro_dataset_factories`, `catalog-data/how_to_use_dataset_factories`,
`catalog-data/partitioned_and_incremental_datasets`, `catalog-data/how_to_use_partitioned_and_incremental_datasets`,
`catalog-data/dataset_validation`, `catalog-data/how_to_access_the_data_catalog_in_code`,
`catalog-data/data_catalog_yaml_examples` (anchors, transcoding), `configure/templating` (oc.env),
`extend/how_to_create_a_custom_dataset`.
