"""Contract checks on node inputs/outputs, configured per dataset name.

Since Kedro 1.6, prefer a `validator` on the catalog entry (runs on every load/save, also outside
runs). Use this hook for cross-cutting rules the catalog can't express, e.g. "no node may emit an
empty DataFrame".

    HOOKS = (DataValidationHook(required_columns={"station_a.clean_obs": {"time", "wave_height"}}),)
"""

import logging
from typing import Any

import pandas as pd
from kedro.framework.hooks import hook_impl
from kedro.pipeline import Node

logger = logging.getLogger(__name__)


class DataValidationHook:
    def __init__(self, required_columns: dict[str, set[str]] | None = None, forbid_empty_outputs: bool = True) -> None:
        # Configuration lives on the instance: hook arguments must not have defaults.
        self._required = {name: set(cols) for name, cols in (required_columns or {}).items()}
        self._forbid_empty = forbid_empty_outputs

    def _check_columns(self, name: str, data: Any) -> None:
        if name in self._required and isinstance(data, pd.DataFrame):
            missing = self._required[name] - set(data.columns)
            if missing:
                raise ValueError(f"Dataset '{name}' is missing required columns: {sorted(missing)}")

    @hook_impl
    def before_node_run(self, node: Node, inputs: dict[str, Any]) -> None:
        for name, data in inputs.items():
            self._check_columns(name, data)

    @hook_impl
    def after_node_run(self, node: Node, outputs: dict[str, Any]) -> None:
        for name, data in outputs.items():
            self._check_columns(name, data)
            if self._forbid_empty and isinstance(data, pd.DataFrame) and data.empty:
                raise ValueError(f"Node '{node.name}' produced an empty DataFrame for '{name}'")
