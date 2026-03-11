import logging
import os
import time
from typing import Any, Dict

from kedro.io import AbstractDataset
from kedro.pipeline.node import Node
from kedro.runner import SequentialRunner

logger = logging.getLogger(__name__)

class TimeBasedCacheRunner(SequentialRunner):
    """
    A Custom Runner that intercepts node execution (Strategy C).
    It checks if ALL output datasets for a given node exist locally 
    and were modified within the last 24 hours. 
    
    If so, it skips both computation and I/O.
    
    To use this, pass it to your session:
    `session.run(runner=TimeBasedCacheRunner())`
    """
    
    CACHE_EXPIRATION_SECONDS = 86400  # 24 hours

    def _run_node(self, node: Node, catalog: Any, hook_manager: Any, session_id: str) -> Dict[str, Any]:
        """
        Intercepts the standard execution. If the cache is valid, it short-circuits.
        Otherwise, it falls back to the parent SequentialRunner execution.
        """
        # 1. Determine if we should attempt caching
        outputs_to_check = node.outputs
        
        # We can't cache nodes that don't output anything, or return MemoryDatasets
        if not outputs_to_check:
            return super()._run_node(node, catalog, hook_manager, session_id)

        all_outputs_cached = True
        
        for output_name in outputs_to_check:
            try:
                # 2. Extract the physical filepath from the Dataset class in the Catalog
                dataset: AbstractDataset = catalog._datasets[output_name]
                
                # Check if it has a filepath attribute (e.g. CSVDataset, ParquetDataset)
                if not hasattr(dataset, '_filepath'):
                    all_outputs_cached = False
                    break
                
                filepath = str(dataset._filepath)
                
                # 3. Check exact existence and modification timestamp
                if not os.path.exists(filepath):
                    all_outputs_cached = False
                    break
                    
                mtime = os.path.getmtime(filepath)
                age_seconds = time.time() - mtime
                
                if age_seconds > self.CACHE_EXPIRATION_SECONDS:
                    logger.info(f"Cache expired for {output_name} ({age_seconds/3600:.1f} hours old)")
                    all_outputs_cached = False
                    break
                    
            except Exception as e:
                # Fallback to standard execution on any resolution issues
                logger.debug(f"Could not check cache for {output_name}: {e}")
                all_outputs_cached = False
                break
                
        # 4. Short-Circuit if fully cached!
        if all_outputs_cached:
            logger.warning(f"⏩ SKIPPING NODE '{node.name}'. All outputs exist and are < 24 hours old.")
            # By returning an empty dict, we tell the Runner this node is "done" without executing it.
            return {}
            
        # 5. Fallback: Execute the node normally
        return super()._run_node(node, catalog, hook_manager, session_id)
