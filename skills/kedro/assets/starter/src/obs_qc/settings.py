"""Project settings. Only non-default values are set."""

from kedro.config import OmegaConfigLoader

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    # Deep-merge parameters across envs and with --params, so overriding one nested key
    # (kedro run --params station_a.qc.min_quality=3) keeps its siblings.
    "merge_strategy": {"parameters": "soft"},
}
