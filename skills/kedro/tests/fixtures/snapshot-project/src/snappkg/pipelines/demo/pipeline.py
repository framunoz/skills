"""Deliberately flawed pipeline: every kind of snapshot finding appears once."""

from kedro.pipeline import Node, Pipeline


def clean(raw, min_quality):
    return raw


def enrich(clean_obs, stations):
    return clean_obs


def summarise(enriched, threshold):
    return {"rows": len(enriched)}


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(clean, ["raw_obs", "params:cleaning.min_quality"], "clean_obs", name="clean"),
            Node(enrich, ["clean_obs", "stations"], "enriched"),          # stations undeclared; no name
            Node(summarise, ["enriched", "params:thresholds"], "summary", name="summarise"),  # bad param
        ]
    )
