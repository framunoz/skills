import logging
import time

from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node

logger = logging.getLogger(__name__)

class NodeTimingHook:
    """
    A simple hook that measures the exact execution time of every node
    and logs it. It also catches any errors and logs them prominently.
    
    To activate this, add `NodeTimingHook()` to your `HOOKS` tuple in `settings.py`.
    """
    
    def __init__(self):
        self._start_times = {}

    @hook_impl
    def before_node_run(self, node: Node) -> None:
        """Runs immediately before a node executes."""
        self._start_times[node.name] = time.time()
        logger.info(f"🚀 Starting node: {node.name}")

    @hook_impl
    def after_node_run(self, node: Node) -> None:
        """Runs immediately after a node executes successfully."""
        start_time = self._start_times.get(node.name)
        if start_time:
            duration = time.time() - start_time
            logger.info(f"✅ Node {node.name} completed in {duration:.2f} seconds.")

    @hook_impl
    def on_node_error(self, error: Exception, node: Node) -> None:
        """Runs if a node raises an exception."""
        start_time = self._start_times.get(node.name)
        if start_time:
            duration = time.time() - start_time
            logger.error(f"❌ Node {node.name} FAILED after {duration:.2f} seconds.")
        logger.error(f"Error details: {error}")
        
        # NOTE: You could add a Slack or MS Teams webhook call here!
        # Just ensure you wrap that external call in a try/except so it doesn't mask the original error.
