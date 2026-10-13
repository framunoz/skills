"""Pure functions: no I/O, no Kedro imports — the catalog handles loading and saving."""

import pandas as pd
from pydantic import BaseModel, Field


class QCParams(BaseModel):
    """Validated before any node runs (typed params, Kedro >= 1.3)."""

    min_quality: int = Field(ge=0, le=4)
    max_wave_height: float = Field(gt=0)


def clean_observations(raw: pd.DataFrame, qc: QCParams) -> pd.DataFrame:
    keep = (raw["quality"] >= qc.min_quality) & (raw["wave_height"] <= qc.max_wave_height)
    return raw.loc[keep].sort_values("time").reset_index(drop=True)


def summarise(clean: pd.DataFrame) -> dict:
    return {
        "rows": int(len(clean)),
        "mean_wave_height": round(float(clean["wave_height"].mean()), 3),
        "max_wave_height": float(clean["wave_height"].max()),
    }
