"""Unit test for nodes + pipeline test with in-memory data (no files, no config)."""

import pandas as pd
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from obs_qc.pipelines.qc.nodes import QCParams, clean_observations
from obs_qc.pipelines.qc.pipeline import base_pipeline

RAW = pd.DataFrame(
    {"time": pd.date_range("2026-01-01", periods=3, freq="h"), "wave_height": [1.0, 30.0, 2.0], "quality": [4, 4, 0]}
)


def test_clean_observations_drops_bad_rows():
    out = clean_observations(RAW, QCParams(min_quality=1, max_wave_height=10))
    assert out["wave_height"].tolist() == [1.0]


def test_pipeline_runs_in_memory():
    # The runner does not validate typed params: pass the model instance, not a dict.
    catalog = DataCatalog(
        {"raw_obs": MemoryDataset(RAW), "params:qc": MemoryDataset(QCParams(min_quality=1, max_wave_height=10))}
    )
    outputs = SequentialRunner().run(base_pipeline(), catalog)
    summary = outputs["qc_summary"].load()  # run() returns dataset objects, not data
    assert summary["rows"] == 1
