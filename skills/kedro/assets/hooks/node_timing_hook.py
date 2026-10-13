"""Log each node's duration and failures.

Register an instance in settings.py:  HOOKS = (NodeTimingHook(),)
Hook arguments are injected by name (pluggy): declare only what you use, never with defaults.
Node hooks don't fire inside ParallelRunner workers.
"""

import logging
import time

from kedro.framework.hooks import hook_impl
from kedro.pipeline import Node

logger = logging.getLogger(__name__)


class NodeTimingHook:
    def __init__(self) -> None:
        self._start: dict[str, float] = {}

    @hook_impl
    def before_node_run(self, node: Node) -> None:
        self._start[node.name] = time.perf_counter()

    @hook_impl
    def after_node_run(self, node: Node) -> None:
        elapsed = time.perf_counter() - self._start.pop(node.name, time.perf_counter())
        logger.info("Node %s took %.2fs", node.name, elapsed)

    @hook_impl
    def on_node_error(self, error: Exception, node: Node) -> None:
        elapsed = time.perf_counter() - self._start.pop(node.name, time.perf_counter())
        logger.error("Node %s failed after %.2fs: %s", node.name, elapsed, error)
        # Alerting (Slack/Teams) goes here — wrap it in try/except so it never masks `error`.
