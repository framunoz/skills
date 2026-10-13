# Project: creation, layout, settings, dependencies

## What makes a directory a Kedro project

Three files, nothing else (docs `create/minimal_kedro_project`):

| File | Role |
|---|---|
| `pyproject.toml` with `[tool.kedro]` | `package_name`, `project_name`, `kedro_init_version`, `source_dir` (default `src`), `tools`, `example_pipeline` |
| `src/<package>/settings.py` | Project settings (may be empty): config loader, hooks, catalog/session classes |
| `src/<package>/pipeline_registry.py` | `register_pipelines() -> dict[str, Pipeline]` |

`kedro_init_version` only has to match the installed Kedro's **major** version (since 1.1.1);
a 0.19 project fails on Kedro 1.x until migrated (`about/migration`).

## Create

```bash
uvx kedro==1.7.0 new --name "Ocean Forecast" --tools lint,test,data --example n --telemetry no
cd ocean-forecast && uv sync && uv run kedro run
```

| Flag | Values |
|---|---|
| `--tools` | `lint` (ruff), `test` (pytest), `log`, `docs` (Sphinx), `data` (the `data/01_raw…08_reporting` tree), `pyspark`, `all`, `none` |
| `--example` | `y` adds the spaceflights pipelines (`data_processing`, `data_science`, `reporting`) and data |
| `--starter` | `spaceflights-pandas`, `spaceflights-pyspark`, `databricks-iris`, `astro-airflow-iris`, `support-agent-langgraph` (`kedro starter list`), a local path or a git URL; `--checkout <tag>` pins it |
| `--config file.yml` | Non-interactive: `project_name`, `repo_name`, `python_package` (+ `tools`, `example_pipeline`) |
| `--telemetry no` | Writes `.telemetry` with `consent: false` |

Without `--tools data` there is **no `data/` directory** — create the layer folders you need.
(verified on 1.7.0)

## Layout (template)

```
conf/base/            catalog.yml, parameters*.yml   — committed, shared
conf/local/           credentials.yml                — git-ignored (conf/local/**, conf/**/*credentials*)
data/01_raw … 08_reporting                           — git-ignored (data/**), folders kept
notebooks/
src/<package>/
  settings.py  pipeline_registry.py  __main__.py
  pipelines/<name>/{__init__.py, nodes.py, pipeline.py}
tests/                (with --tools test)
pyproject.toml  requirements.txt  README.md  .gitignore
```

Data-layer convention (also used by Kedro-Viz layers): `01_raw` immutable input →
`02_intermediate` typed/cleaned → `03_primary` domain model → `04_feature` →
`05_model_input` → `06_models` → `07_model_output` → `08_reporting`.

## `settings.py`

Everything is optional; defaults apply when absent.

| Setting | Use |
|---|---|
| `CONFIG_LOADER_CLASS`, `CONFIG_LOADER_ARGS` | `OmegaConfigLoader` + `base_env`, `default_run_env`, `config_patterns`, `merge_strategy`, `custom_resolvers` — see `concepts/configuration.md` |
| `CONF_SOURCE` | Config directory other than `conf` |
| `HOOKS = (MyHooks(),)` | Register hook instances — `concepts/hooks-and-plugins.md` |
| `DISABLE_HOOKS_FOR_PLUGINS` | Turn off auto-registered plugin hooks |
| `DATA_CATALOG_CLASS` | Custom catalog class |
| `CONTEXT_CLASS` | Custom `KedroContext` subclass |
| `SESSION_CLASS` (1.3+) | Custom `KedroSession` subclass |
| `SESSION_STORE_CLASS`/`ARGS` | Session store (e.g. Kedro-Viz `SQLiteStore`) |
| `RUNNER_MODULE_ALLOWLIST` (1.6+, was `RUNNER_MODULES_WHITELIST`) | Modules allowed for `--runner` |
| `DATASET_VALIDATION` (1.6+) | Turn catalog `validator`s off globally |

## Dependencies with uv

The template's `pyproject.toml` already lists `[project] dependencies` (it mirrors
`requirements.txt`), so uv works directly: (verified on 1.7.0)

```bash
uv sync                                     # creates .venv, installs the package editable
uv add "kedro-datasets[pandas-parquetdataset,netcdf-netcdfdataset]"
uv add --dev pytest ruff
uv run kedro run                            # every kedro command through uv run
```

- `uv add` updates `pyproject.toml`/`uv.lock` but **not** `requirements.txt`, which then drifts.
  Make `pyproject.toml` the single source of truth and delete `requirements.txt` (or regenerate
  it with `uv export --no-hashes > requirements.txt` if a platform needs it).
- Dataset dependencies are **extras** of `kedro-datasets`: `<module>-<class>` lower-case
  (`pandas.CSVDataset` → `pandas-csvdataset`). `scripts/check_dataset.py` prints the exact one.
- Pin the minor: `kedro~=1.7.0`. Kedro follows SemVer; breaking changes land in majors
  (0.19 → 1.0), but minors rename settings and add features (see `RELEASE.md`).

## Scaffolding

- `uv run kedro pipeline create <name>` — `src/<package>/pipelines/<name>/` (+ tests,
  + `conf/base/parameters_<name>.yml`); details in `concepts/pipelines.md`.
- `find_pipelines()` in the registry picks the new pipeline up automatically.

## Telemetry

`kedro-telemetry` is pulled in by the template (via `kedro-viz`). Opt out per project with
`.telemetry` (`consent: false`) or globally with `KEDRO_DISABLE_TELEMETRY=1` / `DO_NOT_TRACK=1`.

## More detail

`create/new_project`, `create/minimal_kedro_project`, `create/new_project_tools`,
`create/starters`, `tutorials/settings`, `develop/dependencies`, `about/migration`,
`about/telemetry`.
