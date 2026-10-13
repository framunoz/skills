# Observation QC — Kedro starter (skill asset)

Minimal, render-tested Kedro 1.7 project showing the conventions this skill recommends:
one pipeline reused per station with namespaces, dataset factories with distinct suffixes,
Viz layers in `metadata`, typed (Pydantic) parameters, soft parameter merge, explicit node names.

```bash
uv sync
uv run kedro run                                   # both stations
uv run kedro run --namespaces station_b            # one station
uv run kedro run --params station_a.qc.min_quality=3
uv run pytest
```
