"""Evaluation, predictions, and interpretation helpers."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from feature_engineering import split_features_target


def evaluate_models(models: dict, test_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate test predictions and calculate all requested regression metrics."""
    x_test, y_test = split_features_target(test_data)
    prediction_frame = test_data[["dteday", "hr", "cnt"]].copy()
    rows = []
    for name, model in models.items():
        predictions = model.predict(x_test)
        prediction_frame[f"{name}_prediction"] = predictions
        residuals = y_test.to_numpy() - predictions
        rows.append({
            "model": name,
            "MAE": mean_absolute_error(y_test, predictions),
            "MSE": mean_squared_error(y_test, predictions),
            "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
            "R2": r2_score(y_test, predictions),
            "mean_residual": residuals.mean(),
            "largest_absolute_error": np.abs(residuals).max(),
        })
    return pd.DataFrame(rows), prediction_frame


def feature_importance(model, model_name: str) -> pd.DataFrame:
    """Extract transformed feature importances from a fitted pipeline."""
    preprocessor = model.named_steps["preprocessor"]
    estimator = model.named_steps["model"]
    names = preprocessor.get_feature_names_out()
    return pd.DataFrame({
        "feature": names,
        "importance": estimator.feature_importances_,
        "model": model_name,
    }).sort_values("importance", ascending=False)


def save_results(
    metrics: pd.DataFrame,
    predictions: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Persist measured results for notebooks and README reporting."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output / "model_comparison.csv", index=False)
    predictions.to_csv(output / "test_predictions.csv", index=False)


def largest_errors(
    models: dict,
    test_data: pd.DataFrame,
    predictions: pd.DataFrame,
    limit: int = 20,
) -> pd.DataFrame:
    """Return test observations with the largest absolute prediction errors."""
    records = test_data[[
        "dteday", "hr", "season", "workingday", "weathersit", "temp", "hum", "cnt"
    ]].copy()
    for name in models:
        prediction_column = f"{name}_prediction"
        records[f"{name}_error"] = records["cnt"] - predictions[prediction_column].to_numpy()
        records[f"{name}_absolute_error"] = records[f"{name}_error"].abs()
    records["max_absolute_error"] = records[
        [f"{name}_absolute_error" for name in models]
    ].max(axis=1)
    return records.sort_values("max_absolute_error", ascending=False).head(limit)
