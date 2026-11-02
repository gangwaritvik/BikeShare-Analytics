"""Chronological training and time-series hyperparameter tuning."""

from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

from feature_engineering import split_features_target


RANDOM_STATE = 42
CATEGORICAL_COLUMNS = [
    "season", "yr", "mnth", "hr", "holiday", "weekday", "workingday",
    "weathersit", "day_of_week", "weekend",
]


def _pipeline(model):
    """Build a model pipeline with fitted-on-training one-hot encoding."""
    categorical = [column for column in CATEGORICAL_COLUMNS]
    numeric = [
        "temp", "atemp", "hum", "windspeed", "date_year",
        "hour_sin", "hour_cos", "month_sin", "month_cos",
    ]
    transformer = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", "passthrough", numeric),
        ],
        remainder="drop",
    )
    return Pipeline([("preprocessor", transformer), ("model", model)])


def train_models(
    train_data: pd.DataFrame,
    model_dir: str | Path,
) -> tuple[dict, pd.DataFrame]:
    """Tune both primary models using only the chronological training period."""
    x_train, y_train = split_features_target(train_data)
    cv = TimeSeriesSplit(n_splits=4)
    searches = {
        "random_forest": GridSearchCV(
            _pipeline(RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)),
            {
                "model__n_estimators": [150, 300],
                "model__max_depth": [None, 20],
                "model__min_samples_leaf": [1, 2],
            },
            cv=cv,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1,
            refit=True,
        ),
        "xgboost": GridSearchCV(
            _pipeline(XGBRegressor(
                objective="reg:squarederror",
                random_state=RANDOM_STATE,
                n_jobs=-1,
                tree_method="hist",
            )),
            {
                "model__n_estimators": [300, 600],
                "model__max_depth": [5, 8],
                "model__learning_rate": [0.05, 0.1],
                "model__subsample": [0.8],
                "model__colsample_bytree": [0.9],
            },
            cv=cv,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1,
            refit=True,
        ),
    }
    output_dir = Path(model_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    fitted = {}
    for name, search in searches.items():
        search.fit(x_train, y_train)
        fitted[name] = search.best_estimator_
        joblib.dump(search.best_estimator_, output_dir / f"{name}.joblib")
        results.append({
            "model": name,
            "best_cv_rmse": -search.best_score_,
            "best_params": json.dumps(search.best_params_, sort_keys=True),
        })
    return fitted, pd.DataFrame(results)
