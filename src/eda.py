"""Reproducible exploratory analysis and plot generation."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def run_eda(data: pd.DataFrame, output_dir: str | Path) -> dict:
    """Create the project's meaningful EDA plots and return measured findings."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    frame = data.copy()
    frame["dteday"] = pd.to_datetime(frame["dteday"])
    frame["date_year"] = frame["dteday"].dt.year
    sns.set_theme(style="whitegrid")

    def save(name: str, title: str, xlabel: str, ylabel: str) -> None:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(output / name, dpi=150)
        plt.close()

    plt.figure(figsize=(8, 4))
    sns.histplot(frame["cnt"], bins=50, kde=True)
    save("target_distribution.png", "Hourly Rental Count Distribution", "Rental count (cnt)", "Frequency")

    hourly = frame.groupby("hr", as_index=False)["cnt"].mean()
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=hourly, x="hr", y="cnt", marker="o")
    save("hourly_demand.png", "Average Demand by Hour", "Hour of day", "Mean rental count")

    monthly = frame.groupby(["date_year", "mnth"], as_index=False)["cnt"].mean()
    plt.figure(figsize=(9, 4))
    sns.lineplot(data=monthly, x="mnth", y="cnt", hue="date_year", marker="o")
    save("monthly_demand.png", "Average Monthly Demand by Year", "Month", "Mean rental count")

    for column, filename, title, xlabel in [
        ("season", "seasonal_demand.png", "Demand by Season", "Season code"),
        ("workingday", "workingday_demand.png", "Demand by Working-Day Status", "Working day (0/1)"),
        ("weathersit", "weather_demand.png", "Demand by Weather Situation", "Weather situation code"),
    ]:
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=frame, x=column, y="cnt")
        save(filename, title, xlabel, "Rental count")

    sample = frame.sample(min(5000, len(frame)), random_state=42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.scatterplot(data=sample, x="temp", y="cnt", alpha=0.25, ax=axes[0])
    axes[0].set(title="Temperature and Demand", xlabel="Normalized temperature", ylabel="Rental count")
    sns.scatterplot(data=sample, x="hum", y="cnt", alpha=0.25, ax=axes[1])
    axes[1].set(title="Humidity and Demand", xlabel="Normalized humidity", ylabel="Rental count")
    fig.tight_layout()
    fig.savefig(output / "temperature_humidity_demand.png", dpi=150)
    plt.close(fig)

    numeric = frame.select_dtypes(include=np.number).drop(columns=["casual", "registered"], errors="ignore")
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric.corr(), cmap="coolwarm", center=0)
    save("correlation_heatmap.png", "Correlation Matrix Without Leakage Counts", "Variables", "Variables")

    iqr = frame["cnt"].quantile(0.75) - frame["cnt"].quantile(0.25)
    lower = frame["cnt"].quantile(0.25) - 1.5 * iqr
    upper = frame["cnt"].quantile(0.75) + 1.5 * iqr
    outliers = int(((frame["cnt"] < lower) | (frame["cnt"] > upper)).sum())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.boxplot(y=frame["cnt"], ax=axes[0])
    axes[0].set(title="Target Outlier View", ylabel="Rental count")
    sns.boxplot(data=frame[["temp", "hum", "windspeed"]], ax=axes[1])
    axes[1].set(title="Weather Feature Outlier View", ylabel="Normalized value")
    fig.tight_layout()
    fig.savefig(output / "outlier_boxplots.png", dpi=150)
    plt.close(fig)
    return {
        "shape": list(frame.shape),
        "missing_values": int(frame.isna().sum().sum()),
        "duplicate_rows": int(frame.duplicated().sum()),
        "hourly_peak_hours": hourly.nlargest(2, "cnt")["hr"].astype(int).tolist(),
        "hourly_low_hours": hourly.nsmallest(2, "cnt")["hr"].astype(int).tolist(),
        "target_mean": float(frame["cnt"].mean()),
        "target_median": float(frame["cnt"].median()),
        "iqr_lower": float(lower),
        "iqr_upper": float(upper),
        "iqr_outliers": outliers,
    }
