"""Interactive demand prediction page."""

from datetime import date

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.charts import style_figure
from feature_engineering import make_features
from utils.data_loader import SEASON_LABELS, WEATHER_LABELS


def _category(value: float, train_target: pd.Series) -> tuple[str, str]:
    low, high = train_target.quantile([.33, .66]).tolist()
    if value <= low:
        return "Low demand", f"At or below the 33rd percentile ({low:.0f} rentals)."
    if value <= high:
        return "Moderate demand", f"Between the 33rd ({low:.0f}) and 66th ({high:.0f}) percentiles."
    return "High demand", f"Above the 66th percentile ({high:.0f} rentals)."


def _prediction_distribution(prediction: float, historical: pd.Series):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=historical, nbinsx=45, name="Historical hourly demand",
        marker_color="#334155", opacity=.85,
        hovertemplate="Count: %{y}<br>Rentals: %{x}<extra></extra>",
    ))
    fig.add_vline(x=prediction, line_color="#22c55e", line_width=3, annotation_text=f"Prediction {prediction:.0f}", annotation_position="top")
    fig.update_layout(title="Prediction against historical demand", xaxis_title="Hourly rental count", yaxis_title="Frequency")
    return style_figure(fig, 330)


def render_demand_prediction(data: dict, models: dict) -> None:
    raw, train = data["raw"], data["train"]
    st.markdown('<div class="section-kicker">FORECAST WORKSPACE</div><div class="section-title">Predict hourly bike demand</div><p class="section-description">Enter conditions known before the hour begins. The saved training pipeline handles feature construction and encoding.</p>', unsafe_allow_html=True)
    if not models:
        st.error("No trained model artifact is available. Add the saved .joblib files to models/ before predicting.")
        return

    left, right = st.columns([1.15, .85], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Forecast inputs")
        input_date = st.date_input("Date", value=date(2012, 6, 15), min_value=date(2011, 1, 1), max_value=date(2012, 12, 31))
        c1, c2 = st.columns(2)
        with c1:
            hour = st.slider("Hour of day", 0, 23, 8, format="%02d:00")
            model_name = st.selectbox("Model", list(models.keys()))
            season = st.selectbox("Season", list(SEASON_LABELS.values()), index=1)
            weather = st.selectbox("Weather condition", list(WEATHER_LABELS.values()))
        with c2:
            holiday = st.selectbox("Holiday", ["No", "Yes"])
            workingday = st.selectbox("Working day", ["No", "Yes"], index=1)
            temperature = st.slider("Temperature", 0.02, 1.00, 0.50, .01, help="Normalized UCI temperature value.")
            feeling_temperature = st.slider("Feeling temperature", 0.02, 1.00, 0.48, .01, help="Normalized UCI apparent temperature.")
        c3, c4 = st.columns(2)
        with c3:
            humidity = st.slider("Humidity", 0.00, 1.00, 0.60, .01, help="Normalized UCI humidity value.")
        with c4:
            windspeed = st.slider("Wind speed", 0.00, 0.70, 0.20, .01, help="Normalized UCI wind speed value.")
        predict = st.button("PREDICT BIKE DEMAND", use_container_width=True)
        st.markdown('<div class="fine-print">Inputs use the same normalized weather scale as the UCI dataset. Dates are limited to the observed 2011–2012 period.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        if not predict:
            st.markdown('<div class="prediction-panel"><div class="prediction-label">Ready for forecast</div><div class="prediction-number">—</div><p class="fine-print">Choose conditions and run the saved model to see a measured prediction.</p></div>', unsafe_allow_html=True)
            st.plotly_chart(_prediction_distribution(float(train["cnt"].median()), train["cnt"]), use_container_width=True, config={"displayModeBar": False})
            return
        selected_season = next(code for code, label in SEASON_LABELS.items() if label == season)
        selected_weather = next(code for code, label in WEATHER_LABELS.items() if label == weather)
        row = pd.DataFrame([{
            "dteday": pd.Timestamp(input_date),
            "season": selected_season,
            "yr": int(input_date.year == 2012),
            "mnth": input_date.month,
            "hr": hour,
            "holiday": int(holiday == "Yes"),
            "weekday": pd.Timestamp(input_date).dayofweek,
            "workingday": int(workingday == "Yes"),
            "weathersit": selected_weather,
            "temp": temperature,
            "atemp": feeling_temperature,
            "hum": humidity,
            "windspeed": windspeed,
        }])
        try:
            prediction = float(models[model_name].predict(make_features(row))[0])
        except (KeyError, ValueError, TypeError) as error:
            st.error(f"Prediction could not be generated from the saved model contract: {error}")
            return
        prediction = max(0.0, prediction)
        category, explanation = _category(prediction, train["cnt"])
        st.markdown(f'<div class="prediction-panel"><div class="prediction-label">{model_name} · forecast result</div><div class="prediction-number">{prediction:,.0f}</div><p class="fine-print">{category} · {explanation}</p></div>', unsafe_allow_html=True)
        st.plotly_chart(_prediction_distribution(prediction, train["cnt"]), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f'<div class="insight">This forecast uses hour {hour:02d}:00, {season.lower()} conditions, and the selected weather inputs. It is an estimate from the trained model, not an observed count.</div>', unsafe_allow_html=True)
