"""Feature engineering for hourly bike-demand prediction."""

import numpy as np
import pandas as pd


TARGET = "cnt"
LEAKAGE_COLUMNS = {"cnt", "casual", "registered", "instant", "dteday"}


def make_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create predictors using only fields known before the rental count."""
    frame = data.copy()
    frame["dteday"] = pd.to_datetime(frame["dteday"], errors="raise")
    frame["date_year"] = frame["dteday"].dt.year
    frame["day_of_week"] = frame["dteday"].dt.dayofweek
    frame["weekend"] = frame["day_of_week"].isin([5, 6]).astype(int)
    frame["hour_sin"] = np.sin(2 * np.pi * frame["hr"] / 24)
    frame["hour_cos"] = np.cos(2 * np.pi * frame["hr"] / 24)
    frame["month_sin"] = np.sin(2 * np.pi * (frame["mnth"] - 1) / 12)
    frame["month_cos"] = np.cos(2 * np.pi * (frame["mnth"] - 1) / 12)
    return frame.drop(columns=[column for column in LEAKAGE_COLUMNS if column in frame])


def split_features_target(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return model predictors and target, explicitly excluding leakage fields."""
    if TARGET not in data:
        raise ValueError("The target column 'cnt' is required.")
    return make_features(data), data[TARGET].copy()


def feature_columns() -> list[str]:
    """Return the raw numeric predictor columns used by the models."""
    return [
        "season", "yr", "mnth", "hr", "holiday", "weekday", "workingday",
        "weathersit", "temp", "atemp", "hum", "windspeed", "date_year",
        "day_of_week", "weekend", "hour_sin", "hour_cos", "month_sin",
        "month_cos",
    ]
