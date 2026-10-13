"""One QC pipeline, reused per station through namespaces."""

from kedro.pipeline import Node, Pipeline

from .nodes import clean_observations, summarise

STATIONS = ["station_a", "station_b"]


def base_pipeline() -> Pipeline:
    # Explicit names: --nodes/--from-nodes need them (default names are func__<hash>).
    return Pipeline(
        [
            Node(clean_observations, ["raw_obs", "params:qc"], "clean_obs", name="clean_observations"),
            Node(summarise, "clean_obs", "qc_summary", name="summarise"),
        ],
        tags="qc",
    )


def create_pipeline(**kwargs) -> Pipeline:
    # namespace prefixes node names, datasets (station_a.raw_obs) and params (params:station_a.qc)
    return sum(Pipeline(base_pipeline(), namespace=station) for station in STATIONS)
