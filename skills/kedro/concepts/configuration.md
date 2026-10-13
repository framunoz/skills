# Configuration: conf/, environments, parameters, credentials

Kedro 1.7.0. Loader is always `OmegaConfigLoader` (`ConfigLoader`/`TemplatedConfigLoader` were
removed in 0.19). Reads `.yml`, `.yaml`, `.json`.

## Layout and environments

```
conf/
├── base/                  # shared, committed
│   ├── catalog.yml
│   ├── parameters.yml
│   ├── parameters_<pipeline>.yml
│   └── globals.yml        # optional
├── local/                 # personal + secrets, gitignored (credentials.yml lives here)
└── prod/                  # custom env, optional
```

| Run | Environments loaded (later overrides earlier) |
|---|---|
| `kedro run` | `base` → `local` (`default_run_env`) |
| `kedro run --env prod` / `-e prod` | `base` → `prod` only; **`local` is NOT loaded** (verified on 1.7.0) |
| `KEDRO_ENV=prod kedro run` | same as `--env prod`; `--env` wins if both given (verified on 1.7.0) |

- `base_env` and `default_run_env` folders must exist: a missing `conf/local/` or unknown `--env`
  → `MissingConfigException: Given configuration path either does not exist or is not a valid
  directory: …` (verified on 1.7.0). Keep `conf/local/.gitkeep`.
- Template `.gitignore` ignores `conf/local/**` (except `.gitkeep`) and `conf/**/*credentials*`.

## settings.py: `CONF_SOURCE` and `CONFIG_LOADER_ARGS`

```python
# src/<pkg>/settings.py
from kedro.config import OmegaConfigLoader
from omegaconf.resolvers import oc

CONF_SOURCE = "conf"                       # default
CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",            # "base" = single-env project
    "config_patterns": {                   # adds/replaces per key; others keep defaults
        "spark": ["spark*", "spark*/**"],
        "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
    },
    "merge_strategy": {"parameters": "soft"},          # per key: "destructive" (default) | "soft"
    "custom_resolvers": {"add": lambda *a: sum(a)},    # ${add:1,2,3} → 6
}
```

Default `config_patterns` keys in 1.7.0: `catalog`, `parameters`, `credentials`, `globals`
(verified; docs also list `logging`, but it is not a loader key). Each is
`["<key>*", "<key>*/**", "**/<key>*"]`, except `globals: ["globals.yml"]`. So
`parameters_ds.yml`, `parameters/x.yml`, `sub/parameters_s.yml`, `parameters_j.json` all load;
`params.yml` does not (verified on 1.7.0). Asking for an undeclared key →
`KeyError: "No config patterns were found for 'spark' in your config loader"`.

Other loader args: `ignore_hidden=True` (skip dot-files/dirs), `runtime_params`, `env`.

## Merge rules (verified on 1.7.0)

| Situation | Result |
|---|---|
| catalog/credentials: same top-level key in 2 files, **same env** | `ValueError: Duplicate keys found in <f1> and <f2>: ds` |
| parameters: same **full key path** in 2 files, same env | `ValueError: Duplicate keys found in …: model_options.test_size` (checked at every depth: `a.b.c`) |
| parameters: different sub-keys under one top-level key, same env | deep-merged, no error |
| same top-level key in `base` and `local`/`--env` (default `destructive`) | override env's value **replaces the whole top-level key**; siblings lost. `base: {model_options: {test_size, random_state}}` + `local: {model_options: {test_size: 0.5}}` → `{model_options: {test_size: 0.5}}` |
| same, with `merge_strategy: {parameters: soft}` | deep merge → `{test_size: 0.5, random_state: 3}` |
| credentials across envs (destructive) | `local: c: {a: 9}` drops `base`'s `c.b` |

Hidden `_` keys (verified on 1.7.0 — docs say they are dropped everywhere; not true for parameters):

| Config | Top-level `_key` |
|---|---|
| catalog, credentials, globals | removed from result; usable for `${_key}` interpolation; never a duplicate error |
| parameters | **kept** (`params:_key` exists in the catalog); duplicates across files raise no error and one value silently wins |

Only top-level `_` keys are special; nested `_x` inside a catalog entry stays.

## Parameters

```yaml
# conf/base/parameters_data_science.yml
model_options:
  test_size: 0.2
  random_state: 3
```

| Node input | Receives |
|---|---|
| `"params:model_options"` | dict `{test_size: 0.2, random_state: 3}` |
| `"params:model_options.test_size"` | `0.2` (every nested key is its own catalog entry) |
| `"parameters"` | whole merged dict, including runtime params |

Interpolation `${data.size}` works across all files matching the **same** pattern in the **same**
env; not base→local (`InterpolationKeyError: Interpolation key 'data.size' not found`) and not
catalog→parameters. Use `globals` for cross-type values (verified on 1.7.0).

### `--params` (CLI runtime params)

```bash
kedro run --params "model_options.test_size=0.3,run_date=2026-01-01,flag=true"
```

Parsed with `OmegaConf.from_dotlist` after splitting on `,` and the first `=` (verified on 1.7.0):

| Input | Value |
|---|---|
| `x=1` / `x=007` / `x=1e-3` | `1` / `7` / `0.001` |
| `x=true` / `x=null` | `True` / `None` |
| `x='0.5'` | `"0.5"` (string) |
| `x={a: 1}` | `{"a": 1}` |
| `x=a b` (whole option quoted) | `"a b"` |
| `x=y=z` | `"y=z"` |
| `x=[1,2]` | **error** — comma splits the item: ``Item `2]` must contain a key and a value separated by `=` `` |
| `x:1` | **error** — `=` is required (the docs' `training.learning_rate:0.1` example is wrong) |
| `--params a=1 --params b=2` | only `b` survives (last option wins) |

Dotted keys become nested dicts and merge into parameters like an override env:

- No parameters file in the override env → soft merge, siblings kept.
- Override env (`local` or `--env X`) has **any** parameters file, even empty or unrelated →
  destructive: `--params model_options.test_size=0.3` → `model_options == {test_size: 0.3}`.
- `merge_strategy: {parameters: soft}` → siblings kept in both cases.
(all verified on 1.7.0)

Runtime keys not present in config are added to parameters.

### `${runtime_params:...}` resolver

```yaml
# parameters.yml or catalog.yml (any config type except globals)
model_options:
  random_state: ${runtime_params:seed}                       # required → error if not passed
companies:
  filepath: ${runtime_params:folder, data/01_raw}/companies.csv
seed2: ${runtime_params:seed, ${globals:default_seed}}       # globals as fallback
```

Errors (verified on 1.7.0): missing and no default → `InterpolationResolutionError: Runtime parameter
'seed' not found and no default value provided.`; in `globals.yml` →
``UnsupportedInterpolationType: The `runtime_params:` resolver is not supported for globals.``
A manually built `OmegaConfigLoader` doesn't see CLI `--params`; pass `runtime_params=` yourself.

### Globals

```yaml
# conf/base/globals.yml (local/globals.yml overrides per key)
default_seed: 45
types: {csv: pandas.CSVDataset}
```
Use `${globals:default_seed}`, `${globals:types.csv}`, `${globals:missing, 23}` in parameters and
catalog. Missing without default → `InterpolationResolutionError: Globals key 'nope' not found and no
default value provided.` `_` keys in globals are dropped (verified on 1.7.0).

### Resolvers

- All OmegaConf built-ins work except `oc.env`, which is enabled **only in credentials**.
  In parameters/catalog: `UnsupportedInterpolationType: Unsupported interpolation type oc.env`
  (verified on 1.7.0). To allow it everywhere (discouraged):
  `CONFIG_LOADER_ARGS = {"custom_resolvers": {"oc.env": oc.env}}`.
- Custom resolvers return any Python object (e.g. `"polars": lambda x: getattr(pl, x)` →
  `${polars:Float64}` as a dtype in `load_args`).
- With omegaconf 2.4, every run logs a `UserWarning: register_new_resolver() is deprecated` from
  Kedro's own code — harmless noise (verified on 1.7.0).

### Typed parameter validation (1.3+; scoped to the run's pipelines since 1.4)

Type-hint a node argument fed by `params:` with a Pydantic v2 model or a dataclass; Kedro
converts and validates **before any node runs**, including `--params` overrides.

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field

class Train(BaseModel):
    lr: float = Field(gt=0, le=1)
    epochs: int

@dataclass
class Ev:
    metric: str
    threshold: float

def fit(data, tp: Train, ev: Ev): ...          # tp is a Train, not a dict
Node(fit, ["model_input", "params:train", "params:ev"], "model")
```

- `kedro run --pipelines typed --params train.lr=5` → `ParameterValidationError: Parameter validation
  failed: - Parameter 'train': Failed to instantiate Train … Input should be less than or equal to 1`
  (verified on 1.7.0).
- Dataclasses don't type-check: `--params ev.threshold=abc` passed as `'abc'` (verified on 1.7.0).
- Only pipelines selected with `--pipeline(s)` are inspected: the same bad value did not block
  `--pipeline dbg` (verified on 1.7.0). `--pipeline` is deprecated in 1.7 in favour of
  `--pipelines` (warning on every run).
- `context.params["train"]` also returns the model instance (verified on 1.7.0).
- `Optional[Model]` is unwrapped; `ModelA | ModelB` and plain types are not validated (docs).
- Needs `pydantic>=2` (`kedro[pydantic]`).

## Credentials

```yaml
# conf/local/credentials.yml  (gitignored)
dev_s3:
  key: ${oc.env:AWS_ACCESS_KEY_ID}
  secret: ${oc.env:AWS_SECRET_ACCESS_KEY, ""}   # default avoids error when unset
```
```yaml
# conf/base/catalog.yml
raw:
  type: pandas.CSVDataset
  filepath: s3://bucket/raw.csv
  credentials: dev_s3          # name of top-level key in credentials
```

- The credentials dict is passed to the dataset (fsspec datasets put it in `storage_options`)
  (verified on 1.7.0).
- Unset env var without default → `InterpolationResolutionError: KeyError raised while resolving
  interpolation: "Environment variable 'X' not found"` (verified).
- Unknown name, e.g. credentials only in `local` and run with `--env prod` → `KeyError: "Unable to
  find credentials 'my_creds': check your data catalog and credentials configuration. …"` (verified).
- AWS datasets also pick up `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` from the environment with
  no credentials entry (docs).

## `--conf-source`

```bash
kedro run --conf-source=path/to/conf_dir
kedro run --conf-source=conf.tar.gz        # or .zip
kedro run --conf-source=s3://bucket/conf/  # fsspec protocols; auth via env/cloud CLI, not credentials.yml
```
- Directory, `.tar.gz` and `.zip` all work (verified on 1.7.0). The archive must contain **one
  top-level folder** holding `base/` and `local/`; a flat archive fails with
  `MissingConfigException: … prod/base` (verified). Compressed files on cloud storage are not
  supported (docs).
- Build an archive without secrets: `tar --exclude=local/*.yml -czf conf.tar.gz --directory=<parent> conf`.
- Permanent change: `CONF_SOURCE = "other_conf"` in settings.py.

## Programmatic access

```python
from kedro.config import OmegaConfigLoader, MissingConfigException

cl = OmegaConfigLoader(
    conf_source="conf", base_env="base", default_run_env="local",   # REQUIRED for a project conf/
    env="prod",                                   # optional override env
    runtime_params={"model_options": {"test_size": 0.3}},  # nested dict, not "a.b" keys
)
params = cl["parameters"]
try:
    creds = cl["credentials"]
except MissingConfigException:                    # no file matched the pattern
    creds = {}
cl["catalog"] = {...}                             # bypass loading for one key
```

- Without `base_env`/`default_run_env`, the loader has **no** environments and scans `conf/`
  recursively as one env → `ValueError: Duplicate keys found …` as soon as base and another env
  share a key (verified on 1.7.0).
- `runtime_params={"a.b": 1}` is NOT unflattened — it adds a literal `"a.b"` key. Only the CLI
  converts dotted keys (verified on 1.7.0).
- Inside a project prefer the session, which uses settings.py and CLI params:
  ```python
  from kedro.framework.startup import bootstrap_project
  from kedro.framework.session import KedroSession
  bootstrap_project(".")
  with KedroSession.create(".", env="prod", runtime_params={"seed": 1}) as s:
      ctx = s.load_context()
      ctx.params, ctx.config_loader["catalog"], ctx.catalog
  ```

## More detail

`configure/configuration_basics`, `configure/how_to_configure_project`,
`configure/parameters_and_credentials`, `configure/how_to_use_parameters_and_credentials`,
`configure/templating`, `configure/how_to_use_templating`,
`api/config/kedro.config.OmegaConfigLoader` — see `references.md` for URLs.
