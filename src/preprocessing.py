"""Data loading and leakage-safe dataset preparation."""

from pathlib import Path
from typing import Tuple

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "dataset" / "hour.csv"


def load_hourly_data(data_path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the original UCI hourly bike-sharing dataset."""
    path = Path(data_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place the UCI hour.csv file in dataset/."
        )

    return pd.read_csv(path)


def validate_dataset(data: pd.DataFrame) -> None:
    """Validate the columns required by the project."""
    required = {
        "instant", "dteday", "season", "yr", "mnth", "hr", "holiday",
        "weekday", "workingday", "weathersit", "temp", "atemp", "hum",
        "windspeed", "casual", "registered", "cnt",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")


def chronological_split(
    data: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return 2011 training and 2012 test data in chronological order."""
    prepared = data.copy()
    prepared["dteday"] = pd.to_datetime(prepared["dteday"], errors="raise")
    prepared = prepared.sort_values(["dteday", "hr", "instant"]).reset_index(drop=True)
    train = prepared[prepared["yr"] == 0].copy()
    test = prepared[prepared["yr"] == 1].copy()
    if train.empty or test.empty:
        raise ValueError("Both 2011 (yr=0) and 2012 (yr=1) observations are required.")
    return train, test
