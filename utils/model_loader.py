"""Loading and validating the saved model artifacts."""

from pathlib import Path

import joblib


MODEL_FILES = {"Random Forest": "random_forest.joblib", "XGBoost": "xgboost.joblib"}


def load_models(root: str | Path) -> tuple[dict, dict]:
    models = {}
    errors = {}
    model_dir = Path(root) / "models"
    for display_name, filename in MODEL_FILES.items():
        path = model_dir / filename
        try:
            if not path.is_file():
                raise FileNotFoundError(f"Missing artifact: {path}")
            models[display_name] = joblib.load(path)
        except (OSError, ValueError, ImportError) as error:
            errors[display_name] = str(error)
    return models, errors


def model_status(models: dict, errors: dict) -> tuple[str, str]:
    if len(models) == len(MODEL_FILES):
        return "Models loaded", "online"
    if models:
        return "Partial model load", "warning"
    return "Models unavailable", "warning"
