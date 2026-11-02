"""Cached dashboard data preparation."""

from pathlib import Path

import pandas as pd

from preprocessing import load_hourly_data, chronological_split


SEASON_LABELS = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_LABELS = {
    1: "Clear / Partly cloudy",
    2: "Mist / Cloudy",
    3: "Light rain / Snow",
    4: "Heavy rain / Snow",
}


def load_dashboard_data(root: str | Path) -> dict:
    """Load and enrich actual source data and saved evaluation artifacts."""
    root = Path(root)
    raw = load_hourly_data(root / "dataset" / "hour.csv")
    raw["dteday"] = pd.to_datetime(raw["dteday"])
    raw["year"] = raw["dteday"].dt.year
    raw["season_name"] = raw["season"].map(SEASON_LABELS)
    raw["weather_name"] = raw["weathersit"].map(WEATHER_LABELS)
    raw["day_name"] = raw["dteday"].dt.day_name()
    raw["weekend"] = (raw["dteday"].dt.dayofweek >= 5).astype(int)
    train, test = chronological_split(raw)
    metrics_path = root / "outputs" / "model_comparison.csv"
    cv_path = root / "outputs" / "cross_validation_results.csv"
    predictions_path = root / "outputs" / "test_predictions.csv"
    importances = {}
    for model_name in ("random_forest", "xgboost"):
        path = root / "outputs" / f"{model_name}_feature_importance.csv"
        if path.is_file():
            importances[model_name] = pd.read_csv(path)
    return {
        "raw": raw,
        "train": train,
        "test": test,
        "metrics": pd.read_csv(metrics_path) if metrics_path.is_file() else pd.DataFrame(),
        "cv": pd.read_csv(cv_path) if cv_path.is_file() else pd.DataFrame(),
        "predictions": pd.read_csv(predictions_path) if predictions_path.is_file() else pd.DataFrame(),
        "importances": importances,
    }
