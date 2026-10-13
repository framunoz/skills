# Gotchas

Things that run "fine" but do the wrong thing, or fail far from their cause. Symptom → cause →
fix, grouped by where they bite. All verified on Kedro 1.7.0 unless marked (docs). Details and
exact messages live in the topic file named at the end of each group.

## Environment and versions

- **`ModuleNotFoundError: kedro` / wrong versions / `FileNotFoundError: 'ipython'`** → the shell's
  `python`/`kedro` is not the project env. → Run everything as `uv run kedro …` / `uv run python …`;
  `scripts/kedro_preflight.py` prints the interpreter and whether it is a virtualenv.
- **Project refuses to run after upgrading** → `kedro_init_version` major differs from the
  installed Kedro (0.19 project on 1.x). → Migrate (`about/migration`), then bump it. Minor/patch
  differences are allowed since 1.1.1.
- **`requirements.txt` out of date** → `uv add` only touches `pyproject.toml`/`uv.lock`. → Keep
  `pyproject.toml` as the source of truth; drop or regenerate `requirements.txt`.
- **Every command fails after 1.7.0 with a custom `class:` in `conf/logging.yml`** →
  `ValueError: Module '<pkg>.logutil' specified as a logging class is not permitted…` (new
  allowlist). → `export KEDRO_LOGGING_MODULE_ALLOWLIST=<pkg>.logutil`. `conf/logging.yml` is
  auto-loaded even without `KEDRO_LOGGING_CONFIG`.
- **`UserWarning: register_new_resolver() is deprecated` on every run** → Kedro + omegaconf 2.4.
  Harmless; CLI output (e.g. `kedro catalog …`) is not pure YAML because of these lines.
- **`kedro jupyter setup --help` installs a Jupyter kernel** in the user's kernels dir (the
  `--help` is forwarded). Don't run it to "look at options"; remove `kedro_<pkg>` if created.

## Configuration → `concepts/configuration.md`

- **Siblings vanish with `--params model_options.test_size=0.3`** → if the run env (`local`, or
  `--env X`) has *any* parameters file, the override replaces the whole top-level key
  (destructive merge). → `CONFIG_LOADER_ARGS = {"merge_strategy": {"parameters": "soft"}}`, or a
  `${runtime_params:key, default}` override point, or pass the whole subtree.
- **`--params` syntax**: only `=` works (`a.b:1` fails, though the help/docs show `:`); commas
  split values so lists break (`Item '2]' must contain a key and a value separated by '='`);
  repeating `--params` keeps only the last. → One option, comma-separated, lists in YAML.
- **`runtime_params={"a.b": 1}` in Python is ignored** (CLI unflattens dots, the API does not). →
  Nested dicts.
- **`--env prod` can't find credentials** (`KeyError: "Unable to find credentials 'x'…"`) →
  `local` is *not* loaded with `--env`. → Credentials per env, or `${oc.env:…}` in that env's
  `credentials.yml`.
- **`${oc.env:VAR}` in parameters/catalog** → `UnsupportedInterpolationType`. Allowed only in
  credentials. → `${runtime_params:…}` + `--params "x=$VAR"`; secrets go to credentials.
- **`${runtime_params:…}` in `globals.yml`** → not supported. → `${runtime_params:seed, ${globals:seed}}`.
- **Interpolation across envs or config types** → `InterpolationKeyError`. → `globals.yml`.
- **`params.yml` silently ignored** → default pattern is `parameters*`.
- **Duplicate key error** → same full key path in two parameters files of one env (any depth), or
  same top-level key in two catalog files. Hidden `_keys` in parameters are kept (docs say
  otherwise) and duplicates of them silently pick one.
- **`MissingConfigException: Given configuration path either does not exist…`** → `conf/local/`
  missing (fresh clone without `.gitkeep`), unknown `--env`, or a packaged run without
  `--conf-source`. Archives for `--conf-source` need one top-level folder.
- **`OmegaConfigLoader("conf")` in a script raises duplicate keys** → pass
  `base_env="base", default_run_env="local"`.

## Catalog → `concepts/catalog.md`

- **Output missing from `data/` after a successful run** → not declared in the catalog → it was a
  `MemoryDataset`. `scripts/kedro_snapshot.py` lists these (`memory`, `memory-output`).
- **Namespaced pipeline writes nothing** → namespacing renames datasets (`station_a.clean_obs`), so
  plain entries stop matching and they become memory. → Factory `"{station}.clean_obs"` or explicit
  entries.
- **Experimental dataset "No module named 'netcdf'"** → short `type:` only resolves in
  `kedro_datasets`. → `type: kedro_datasets_experimental.netcdf.NetCDFDataset`.
- **`Dataset 'X' not found in 'pandas'` for a type that exists** (e.g. `SQLTableDataset`) → its
  optional dependency is missing (`sqlalchemy`); the message doesn't say so. → `check_dataset.py`
  shows `imports: FAILS … No module named …` and the extra to add.
- **`Dataset 'CSVDataSet' not found in 'pandas'` / `No module named 'kedro.extras'`** → pre-2.0
  names. → `CSVDataset` from kedro-datasets. `scripts/check_dataset.py` checks names, args, extras.
- **Typo'd or unknown entry key (`layer:`, `load_arg:`)** → no error until a node uses the dataset:
  `__init__() got an unexpected keyword argument 'layer'`. Layers go in
  `metadata: {kedro-viz: {layer: …}}`.
- **Entry without `type`** → the whole session fails, even for unrelated pipelines.
- **Factory captures the wrong object** (`"{x}_train"` as Parquet also caught `y_train`, a Series)
  → `'Series' object has no attribute 'to_parquet'`. → Distinctive suffixes; catch-alls as
  `pickle.PickleDataset`. Ranking is by specificity, never file order; only one catch-all allowed.
- **Versioned dataset saved twice in one catalog** → `Save path … must not exist if versioning is enabled`.
- **0.19 code: `'DataCatalog' object has no attribute 'list'`** (also `add_feed_dict`,
  `_get_dataset`) → removed in 1.0. → `keys()`, `catalog[name] = …`, `catalog[name]`.
- **Empty `PartitionedDataset` folder** → `No partitions found`. `IncrementalDataset` returns `{}`.

## Pipelines and runs → `concepts/pipelines.md`, `concepts/running.md`

- **`--nodes x` / `--from-nodes x` "does not contain nodes named"** → unnamed nodes are
  `func__<hash>` and the hash changes with inputs. → Always `name=`.
- **`kedro run --pipeline x` warns** → deprecated in 1.7. → `--pipelines x[,y]`.
- **Hand-registered pipeline fails with `--pipelines`** (`ImportError … importing the
  '<pkg>.pipelines.<name>' module`) → since 1.5 only `pipelines/<name>/` is imported. → One
  folder with `create_pipeline()` per runnable pipeline. A typo in `--pipelines` gives the same
  error (no suggestion with `raise_errors=True`).
- **`--tags a,b` runs more than expected** → OR, not AND (the slicing doc says AND).
- **Slice fails: `Pipeline input(s) {...} not found in the DataCatalog`** → the slice dropped the
  producer of a memory dataset. → Persist it or widen the slice.
- **`--only-missing-outputs` leaves stale downstream outputs** → existence check, not freshness.
- **Namespaced params "missing"** → `params:qc` becomes `params:station_a.qc`. → Nest the YAML
  under the namespace, or keep it shared with `parameters={"params:qc"}`.
- **Typed-param error blocks a run that doesn't use it** → validation covers the selected
  pipelines, not the `--nodes` slice. Dataclasses are not type-checked — use Pydantic.
  Typing a param in one node converts it for every node that reads it.
- **`--runner-params max_workers=2` → `SequentialRunner.__init__() got an unexpected keyword`** →
  add `--runner ThreadRunner|ParallelRunner`.
- **ParallelRunner: `The following nodes cannot be serialised`** → lambdas/closures; node/dataset
  hooks don't run in workers; cloud datasets may not pickle. → Module-level functions, or ThreadRunner.
- **Generator node into a MemoryDataset passes only the last chunk.**
- **`session.run()` twice → `KedroSessionError: A run has already been completed…`** → new
  session (`%reload_kedro` in notebooks).

## Notebooks, tests, hooks → `concepts/notebooks.md`, `concepts/testing.md`, `concepts/hooks-and-plugins.md`

- **`%load_node` with a function name** → it wants the *node* name; memory inputs can't be loaded.
- **Template `tests/test_run.py` fails from `tests/`** → uses `Path.cwd()`. → Run pytest from the root.
- **Runner in tests passes typed params as dicts** → `'dict' object has no attribute …`. → Pass the
  model instance in the `MemoryDataset`.
- **Hook silently never runs** → misspelled method, missing `@hook_impl`, or a default value on a
  hook argument. `HOOKS = (MyHooks,)` (class, not instance) → `TypeError … forgotten the ()`.
- **`DISABLE_HOOKS_FOR_PLUGINS = ("kedro-mlflow",)` has no effect** → the match is on the
  distribution name verbatim, which is `kedro_mlflow`. → Use the name from
  `entry_points(group="kedro.hooks")` (see `concepts/hooks-and-plugins.md`).
- **"Skip this node if its output is fresh" from a hook** → hooks can't skip nodes (raising
  aborts the run). → Persist the output and slice (`--from-nodes`, `--only-missing-outputs`);
  `kedro-cache` is unmaintained (0.1.1, 2022, Kedro 0.18) — don't recommend it.
- **`kedro viz` ignores project hooks** (e.g. credentials from `after_context_created`) →
  `--include-hooks`.

## MLflow → `concepts/mlflow.md`

- **First run with kedro-mlflow fails: `The filesystem tracking backend (e.g., './mlruns') is in
  maintenance mode`** → MLflow 3.x refuses the file store, and `kedro mlflow init` leaves the URI
  null (= `./mlruns`). → `server.mlflow_tracking_uri: sqlite:///mlflow.db` in `mlflow.yml`.
- **`Run with UUID … is already active`** → kedro-mlflow's hook and a native MLflow hook both
  manage the run. → One path only; disable the plugin as `"kedro_mlflow"`.
- **`matplotlib.MatplotlibWriter` not found** → renamed `matplotlib.MatplotlibDataset`.
- **`PickleDataset … dump() got an unexpected keyword argument 'backend'`** → `backend: joblib`
  is a constructor argument, not a `load_args`/`save_args` key.

## Safety

- **Secrets in `conf/base/`** → committed. → `conf/local/credentials.yml` (git-ignored) or
  `${oc.env:…}` there. Preflight flags `credentials*` under `conf/base`.
- **`kedro server start`** executes pipelines on HTTP requests with no auth; a failed run still
  answers with JSON `"status": "failure"` — check `status`, not only that the call returned. Keep
  the default `127.0.0.1` binding.
