# Recipes

End-to-end patterns. Commands assume uv and the project root as cwd.

## 1. New project with uv

```bash
uvx kedro==1.7.0 new --name "Ocean Forecast" --tools lint,test,data --example n --telemetry no
cd ocean-forecast
uv sync && uv add --dev pytest ruff
rm requirements.txt                       # pyproject.toml is the source of truth
uv run kedro pipeline create ingest
uv run python <skill>/scripts/kedro_preflight.py
```

Or copy `assets/starter/` (namespaced QC pipeline, factories, typed params, soft merge, tests).

## 2. Add a dataset correctly

```bash
uv run python <skill>/scripts/check_dataset.py pandas.ParquetDataset kedro_datasets_experimental.netcdf.NetCDFDataset
uv add "kedro-datasets[pandas-parquetdataset,netcdf-netcdfdataset]"
```

```yaml
# conf/base/catalog.yml
wave_forecast_raw:
  type: kedro_datasets_experimental.netcdf.NetCDFDataset   # experimental → full path
  filepath: data/01_raw/ww3_2026.nc
  metadata: {kedro-viz: {layer: raw}}

wave_features:
  type: pandas.ParquetDataset
  filepath: data/04_feature/wave_features.parquet
  metadata: {kedro-viz: {layer: feature}}
```

Use only arguments the script lists; read the printed docs URL for `load_args`/`save_args`.

## 3. Notebook exploration → node

1. `uv run kedro jupyter lab` (or `%load_ext kedro.ipython` + `%reload_kedro <root>`).
2. `df = catalog.load("wave_features")`; prototype as a **pure function** taking data and params.
3. Move it to `pipelines/<name>/nodes.py`; wire `Node(func, ["wave_features", "params:x"], "out", name="...")`.
4. Declare `out` in the catalog if it must survive the run.
5. `uv run kedro run --pipelines <name>`; then `scripts/kedro_snapshot.py` → no `memory-output`/`param` findings.

## 4. Same pipeline for several entities (stations, regions, models)

`Pipeline(base, namespace=s)` per entity + YAML nested under each namespace + one factory per
artefact (`"{station}.clean_obs"`). Run one with `--namespaces station_b`; override one with
`--params station_b.qc.min_quality=3` (soft merge keeps siblings). Working example:
`assets/starter/`; mapping rules in `concepts/pipelines.md`.

## 5. Experiment with parameters without editing YAML

```python
# settings.py
CONFIG_LOADER_ARGS = {"base_env": "base", "default_run_env": "local",
                      "merge_strategy": {"parameters": "soft"}}
```

```bash
uv run kedro run --pipelines data_science --params "model_options.test_size=0.3,model_options.random_state=7"
```

For values that must come from outside (dates, buckets), declare them:
`run_date: ${runtime_params:run_date, 2026-01-01}` and pass `--params run_date=2026-10-09`.

## 6. Validate parameters up front

Type-hint the node argument with a Pydantic v2 model (`uv add "kedro[pydantic]"`); bad values fail
before any node runs (`ParameterValidationError`). In unit tests pass the model instance.
Example: `assets/starter/src/obs_qc/pipelines/qc/nodes.py`.

## 7. Validate data on load/save (1.6+)

Declare a `validator` (Pandera schema) on the catalog entry — see `concepts/catalog.md`
"Validation". Turn off for one run with `KEDRO_DATASET_VALIDATION=0 uv run kedro run`.

## 8. Re-run part of a pipeline

| Goal | Command |
|---|---|
| From a node to the end | `uv run kedro run --from-nodes clean_observations` |
| Up to an output | `uv run kedro run --to-outputs model_input_table` |
| Only what's missing on disk | `uv run kedro run --only-missing-outputs` (doesn't detect stale files) |
| One entity | `uv run kedro run --namespaces station_b` |
| Load an older model version | `uv run kedro run --load-versions regressor:2026-10-01T12.00.00.000Z` |

Intermediates the slice needs must be persisted, not memory.

## 9. Credentials for cloud data

```yaml
# conf/local/credentials.yml   (git-ignored)
ocean_s3:
  key: ${oc.env:AWS_ACCESS_KEY_ID}
  secret: ${oc.env:AWS_SECRET_ACCESS_KEY}
```

```yaml
# conf/base/catalog.yml
buoy_obs:
  type: pandas.CSVDataset
  filepath: s3://ocean-bucket/buoys/obs.csv
  credentials: ocean_s3
```

For `--env prod`, put an equivalent `conf/prod/credentials.yml` (local isn't loaded).

## 10. Test a pipeline without files

`DataCatalog({"raw_obs": MemoryDataset(df), "params:qc": MemoryDataset(QCParams(...))})` +
`SequentialRunner().run(pipeline, catalog)`; outputs are dataset objects → `.load()`.
Example: `assets/starter/tests/pipelines/test_qc.py`; levels in `concepts/testing.md`.

## 11. Run from Python (script, scheduler, notebook)

```python
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from kedro.runner import SequentialRunner

bootstrap_project(".")
with KedroSession.create(".", env=None, runtime_params={"model_options": {"test_size": 0.3}}) as session:
    out = session.run(pipeline_names=["data_science"], runner=SequentialRunner())
metrics = out["metrics"].load()
```

One `run()` per session; nested dicts for `runtime_params`.

## 12. Package and deploy

`uv run kedro package` → wheel + conf archive in `dist/`; run with
`python -m <package> --conf-source=dist/conf-<package>.tar.gz --env=base`. For orchestrators
group nodes by namespace (`Pipeline.group_nodes_by`) — see `concepts/deployment-and-viz.md`.

## 13. Upgrade a 0.19 project to 1.7

1. `uv run python <skill>/scripts/kedro_preflight.py` → fix every "stale patterns" line.
2. `uv add "kedro~=1.7.0" "kedro-datasets>=9"`; set `kedro_init_version = "1.7.0"`.
3. Replace `--namespace`→`--namespaces`, `--pipeline`→`--pipelines`, `kedro catalog list|rank|resolve`
   → `describe-datasets|list-patterns|resolve-patterns`, removed `DataCatalog` methods,
   `session_id`→`run_id`, `extra_params`→`runtime_params` in hooks.
4. Name all nodes (default names changed in 1.0), run, then `scripts/kedro_snapshot.py`.
5. Official guide: `about/migration`; `kedro-mcp` automates parts of it.
