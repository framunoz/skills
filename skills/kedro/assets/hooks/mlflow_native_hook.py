"""
Native MLflow tracking via Kedro hooks (Path B) — use only when you can't add the
kedro-mlflow plugin, or you need full manual control over the run lifecycle.

Pattern adapted from the official Kedro docs (docs.kedro.org/en/latest/hooks/examples.html).
It scopes a SINGLE MLflow run across the pipeline lifecycle.

⚠️  Do NOT run this alongside kedro-mlflow's auto-registered hook — they will both try to
    manage the run and fight each other. Pick one path.
⚠️  This is a starting template. Validate against your installed mlflow version (the
    flavor API and model logging changed across MLflow 2.x -> 3.x).

To activate, add `MlflowNativeHook()` to your HOOKS tuple in settings.py:

    from <my_project>.hooks import MlflowNativeHook
    HOOKS = (MlflowNativeHook(),)
"""

import logging
from typing import Any, Dict

import mlflow
from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node

logger = logging.getLogger(__name__)


class MlflowNativeHook:
    """Logs params, metrics, and the trained model to a single MLflow run."""

    def __init__(self, experiment_name: str = "default", model_output: str = "trained_model"):
        # Config lives on the instance, never as hook-argument defaults (pluggy gotcha —
        # see references/hooks_architecture.md).
        self._experiment_name = experiment_name
        self._model_output = model_output

    @hook_impl
    def before_pipeline_run(self, run_params: Dict[str, Any]) -> None:
        """Open the run and log run parameters before any node executes."""
        mlflow.set_experiment(self._experiment_name)
        mlflow.start_run(run_name=run_params.get("run_id"))
        mlflow.log_params(run_params)

    @hook_impl
    def after_node_run(self, node: Node, outputs: Dict[str, Any]) -> None:
        """Log any numeric outputs as metrics (skip non-numeric ones)."""
        for name, value in outputs.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(name, value)

    @hook_impl
    def after_pipeline_run(self) -> None:
        """Close the run cleanly when the pipeline finishes successfully."""
        mlflow.end_run()

    @hook_impl
    def on_pipeline_error(self, error: Exception) -> None:
        """Make sure a failure doesn't leave a dangling active run."""
        logger.error(f"Pipeline failed: {error}")
        if mlflow.active_run() is not None:
            mlflow.end_run(status="FAILED")
