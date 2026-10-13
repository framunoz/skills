"""Native MLflow tracking from hooks — only when the kedro-mlflow plugin can't be used.

Never combine with kedro-mlflow on the same run (its auto-registered hook also manages the run);
to test this one in a project that has the plugin: DISABLE_HOOKS_FOR_PLUGINS = ("kedro-mlflow",).

    HOOKS = (MlflowNativeHook(experiment="obs_qc"),)

Verified with mlflow 3.17 / Kedro 1.7. MLflow 3 rejects the ./mlruns file store by default, hence
the sqlite default URI.
"""

import logging
from dataclasses import asdict, is_dataclass
from numbers import Number
from typing import Any

import mlflow
from kedro.framework.hooks import hook_impl
from kedro.pipeline import Node

logger = logging.getLogger(__name__)


def _flatten(prefix: str, value: Any, out: dict[str, Any]) -> None:
    if hasattr(value, "model_dump"):  # typed params arrive as Pydantic models in context.params
        value = value.model_dump()
    elif is_dataclass(value) and not isinstance(value, type):
        value = asdict(value)
    if isinstance(value, dict):
        for key, inner in value.items():
            _flatten(f"{prefix}.{key}" if prefix else str(key), inner, out)
    else:
        out[prefix] = value


class MlflowNativeHook:
    def __init__(self, experiment: str, tracking_uri: str = "sqlite:///mlflow.db") -> None:
        self._experiment = experiment
        self._tracking_uri = tracking_uri
        self._params: dict[str, Any] = {}

    @hook_impl
    def after_context_created(self, context) -> None:
        flat: dict[str, Any] = {}
        _flatten("", context.params, flat)
        self._params = {k: str(v)[:500] for k, v in flat.items()}  # MLflow caps param length

    @hook_impl
    def before_pipeline_run(self, run_params: dict[str, Any]) -> None:
        mlflow.set_tracking_uri(self._tracking_uri)
        mlflow.set_experiment(self._experiment)
        mlflow.start_run(run_name=run_params.get("run_id"))
        mlflow.log_params(self._params)
        mlflow.set_tags({"kedro.pipelines": str(run_params.get("pipeline_names")), "kedro.env": str(run_params.get("env"))})

    @hook_impl
    def after_node_run(self, node: Node, outputs: dict[str, Any]) -> None:
        for name, value in outputs.items():
            if isinstance(value, Number) and not isinstance(value, bool):
                mlflow.log_metric(name, float(value))
            elif isinstance(value, dict) and value and all(isinstance(v, Number) for v in value.values()):
                mlflow.log_metrics({f"{name}.{k}": float(v) for k, v in value.items()})

    @hook_impl
    def after_pipeline_run(self) -> None:
        mlflow.end_run()

    @hook_impl
    def on_pipeline_error(self, error: Exception) -> None:
        logger.error("Pipeline failed: %s", error)
        if mlflow.active_run() is not None:
            mlflow.end_run(status="FAILED")
