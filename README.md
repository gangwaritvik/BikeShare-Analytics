# BikeShare Analytics – Bike Rental Demand Prediction

## Project overview

This project develops a reproducible machine-learning workflow for predicting
hourly bike rental demand (`cnt`) from the UCI Bike Sharing Dataset. It is
designed for a B.Tech CSE Semester 5 Predictive Analytics project and will
cover exploratory analysis, leakage-safe preprocessing, chronological
validation, model training, evaluation, and interpretation.

The repository includes the original `hour.csv` used for the executed
experiments. The source is the UCI
[UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
and the source file is preserved at `dataset/hour.csv`.

## Project structure

```text
BikeShare-Analytics/
├── dataset/hour.csv
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Preprocessing_Feature_Engineering.ipynb
│   ├── 03_Model_Training.ipynb
│   └── 04_Model_Evaluation.ipynb
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── evaluation.py
├── app.py
├── pages/
│   ├── overview.py
│   ├── demand_prediction.py
│   ├── model_comparison.py
│   └── data_insights.py
├── components/
│   ├── charts.py
│   └── styles.py
└── utils/
    ├── data_loader.py
    └── model_loader.py
├── models/
├── outputs/
├── requirements.txt
└── README.md
```

Generated Python caches, virtual environments, secrets, and local editor
settings are excluded by `.gitignore`. The `.joblib` model artifacts are
configured for Git LFS because the Random Forest file exceeds GitHub's normal
100 MB file limit.

## Installation

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The loading utility in `src/preprocessing.py` reads `dataset/hour.csv` and
raises an explicit error when the dataset is missing. No synthetic data is
generated, and the source CSV is never overwritten.

## Methodology

- Use `cnt` as the target and exclude `casual` and `registered` to prevent
  target leakage.
- Use 2011 as the training period and 2012 as the chronological test period.
- Use `TimeSeriesSplit` only within the 2011 training period for tuning.
- Derive hour/day/month, weekend, and sine/cosine cyclical features.
- One-hot encode categorical variables inside each fitted model pipeline.
- Do not automatically delete IQR outliers because unusually high demand can
  be a genuine observation.
- Compare exactly two primary regressors: Random Forest and XGBoost.
- Report MAE, MSE, RMSE, and R² from actual predictions only.

## Running the project

Run the notebooks from the project root in this order:

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks\01_EDA.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks\02_Preprocessing_Feature_Engineering.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks\03_Model_Training.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks\04_Model_Evaluation.ipynb
```

The notebooks write plots and CSV reports to `outputs/` and fitted pipelines
to `models/`. The trained models and reports in this workspace were generated
from the original UCI `hour.csv`.

## Streamlit dashboard

Launch the premium analytics dashboard from the project root:

```powershell
streamlit run app.py
```

The dashboard loads the saved Random Forest and XGBoost pipelines from
`models/`, the original data from `dataset/hour.csv`, and measured evaluation
artifacts from `outputs/`. It does not retrain models or generate synthetic
predictions. The Demand Prediction page uses the shared
`src/feature_engineering.py` contract and excludes `casual`, `registered`, and
`cnt` from prediction inputs.

## Publishing to GitHub

Install Git LFS before adding the model files:

```powershell
git lfs install
git lfs track "models/*.joblib"
```

Then create a GitHub repository and run these commands from this project
directory:

```powershell
git init
git add .
git commit -m "Initial BikeShare Analytics project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/BikeShare-Analytics.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and use the exact repository
URL created on GitHub. Verify that `git lfs ls-files` lists both model files
before pushing.

## Streamlit Community Cloud

After pushing to GitHub:

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Select the repository and the `main` branch.
3. Set the main file to `app.py`.
4. Deploy.

The committed dataset, reports, and Git LFS model artifacts allow the hosted
dashboard to load the same trained models without retraining.

Dashboard sections:

- **Overview** — actual KPI summaries and interactive demand charts.
- **Demand Prediction** — validated date, time, weather, and calendar inputs
  passed to either saved model.
- **Model Comparison** — saved 2012 metrics, diagnostic plots, and feature
  importance comparisons.
- **Data Insights** — filterable exploration of the original hourly records.

## Measured results

The following results were calculated on the chronological 2012 test period
(8,734 rows), after tuning only on 2011:

| Model | MAE | MSE | RMSE | R² |
|---|---:|---:|---:|---:|
| Random Forest | 88.78 | 15,491.995 | 124.47 | 0.6450 |
| XGBoost | 89.68 | 15,465.121 | 124.36 | 0.6456 |

XGBoost has the slightly lower test RMSE and higher R² in this run. The
training-period cross-validation RMSE was 65.16 for Random Forest and 62.66
for XGBoost, so the higher chronological test error also indicates a
distribution shift between the training and future periods.

## Evidence-based observations

- The dataset has 17,379 rows, zero missing values, and zero duplicate rows.
- Average demand is highest at hours 17, 18, and 8 (461.45, 425.51, and
  359.01 rentals respectively).
- Average demand is 193.21 on working days versus 181.41 on non-working days.
- Average demand decreases across the recorded weather severity codes from
  204.87 in code 1 to 111.58 in code 3; code 4 has only a small number of
  observations and should be interpreted cautiously.
- Temperature has a moderate positive correlation with demand (0.405), while
  humidity has a moderate negative correlation (-0.323). Correlation is
  descriptive, not causal.
- The largest held-out absolute error was 569.78 rentals for Random Forest and
  563.19 for XGBoost. The saved `outputs/largest_prediction_errors.csv`
  contains their timestamps, hours, weather, and residuals for inspection.
- Both models rank cyclical hour features among their most important
  predictors. Working-day indicators, temperature, season, and weather also
  appear among the leading transformed features.

## Limitations and future improvements

- The data covers one city and two years, so results may not generalize to
  other locations or future structural changes.
- Weather variables are normalized measurements and the supplied data does not
  capture all events, promotions, station availability, or disruptions.
- The models predict aggregate hourly demand rather than uncertainty
  intervals, and tree importance is not causal explanation.
- Future work could add rolling historical demand features using strictly
  lagged values, probabilistic prediction intervals, calibration by season,
  and external event or station-capacity data.

## Completion status

All six requested phases are complete. The notebooks were executed
sequentially against the official UCI dataset, and the reported results are
the measured outputs of that execution rather than fabricated values.
