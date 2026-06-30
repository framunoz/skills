import logging
from typing import Any, Dict

import pandas as pd
from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node

logger = logging.getLogger(__name__)

class DataValidationHook:
    """
    A hook that intercepts inputs and outputs of nodes to perform schema validation.
    This example validates that any pandas DataFrame meets expected schema requirements
    without polluting the pure functions of the nodes themselves.
    
    To activate this, add `DataValidationHook()` to your `HOOKS` tuple in `settings.py`.
    """

    @hook_impl
    def before_node_run(self, node: Node, inputs: Dict[str, Any]) -> None:
        """Runs before a node executes, validating the input data."""
        for dataset_name, data in inputs.items():
            if isinstance(data, pd.DataFrame):
                logger.info(f"🔎 Validating *input* dataset: '{dataset_name}' for node '{node.name}'")
                
                # Example 1: Generic Data Quality Check (e.g., Warning on NaNs)
                # You might want to skip this for raw data, but enforce it for features.
                if "feature" in dataset_name and data.isnull().any().any():
                    logger.warning(f"⚠️ Quality Warning: Input '{dataset_name}' contains NaN values!")
                
                # Example 2: Strict Schema Check based on dataset naming convention
                if "model_input" in dataset_name:
                    required_columns = {"user_id", "target", "prediction_score"}
                    missing_cols = required_columns - set(data.columns)
                    
                    if missing_cols:
                        # Crashing the pipeline strictly if a schema contract is broken
                        raise ValueError(
                            f"❌ Schema Validation Failed! "
                            f"Dataset '{dataset_name}' is missing required columns: {missing_cols}"
                        )
                
                # Example 3: Type validation
                if "target" in data.columns and not pd.api.types.is_numeric_dtype(data["target"]):
                    raise TypeError(f"❌ Type Validation Failed! Column 'target' must be numeric in '{dataset_name}'.")


    @hook_impl
    def after_node_run(self, node: Node, outputs: Dict[str, Any]) -> None:
        """Runs after a node executes, validating the produced outputs."""
        for dataset_name, data in outputs.items():
            if isinstance(data, pd.DataFrame):
                logger.info(f"🔎 Validating *output* dataset: '{dataset_name}' from node '{node.name}'")
                
                # Example 4: Sanity Check - Ensure the node didn't accidentally drop all rows
                if data.empty:
                    raise ValueError(
                        f"❌ Output Validation Failed! "
                        f"Node '{node.name}' produced an entirely empty DataFrame for '{dataset_name}'."
                    )
