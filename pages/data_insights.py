"""Interactive historical data exploration."""

import plotly.express as px
import streamlit as st

from components.charts import heatmap, style_figure


def render_data_insights(data: dict) -> None:
    raw = data["raw"]
    st.markdown('<div class="section-kicker">HISTORICAL EXPLORER</div><div class="section-title">Find the demand signals</div><p class="section-description">Filter the actual hourly dataset and inspect how time, weather, and working-day context move together.</p>', unsafe_allow_html=True)
    with st.container():
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            seasons = st.multiselect("Season", sorted(raw["season_name"].unique()), default=sorted(raw["season_name"].unique()))
        with c2:
            months = st.multiselect("Month", sorted(raw["mnth"].unique()), default=sorted(raw["mnth"].unique()))
        with c3:
            hours = st.multiselect("Hour", sorted(raw["hr"].unique()), default=sorted(raw["hr"].unique()))
        with c4:
            weather = st.multiselect("Weather", sorted(raw["weather_name"].unique()), default=sorted(raw["weather_name"].unique()))
        with c5:
            working = st.multiselect("Working day", ["Working day", "Non-working day"], default=["Working day", "Non-working day"])
    filtered = raw[
        raw["season_name"].isin(seasons)
        & raw["mnth"].isin(months)
        & raw["hr"].isin(hours)
        & raw["weather_name"].isin(weather)
        & raw["workingday"].map({1: "Working day", 0: "Non-working day"}).isin(working)
    ]
    st.markdown(f'<div class="insight">{len(filtered):,} observations match the current filters. All charts below are recalculated from those rows.</div>', unsafe_allow_html=True)
    if filtered.empty:
        st.info("No observations match the selected filters. Choose at least one value in each filter group.")
        return
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(style_figure(px.histogram(filtered, x="cnt", nbins=45, title="Filtered demand distribution", labels={"cnt": "Hourly rentals"}), 340), use_container_width=True, config={"displayModeBar": False})
    with c2:
        hourly = filtered.groupby("hr", as_index=False)["cnt"].mean()
        st.plotly_chart(style_figure(px.line(hourly, x="hr", y="cnt", markers=True, title="Filtered hourly demand", labels={"hr": "Hour", "cnt": "Mean rentals"}), 340), use_container_width=True, config={"displayModeBar": False})
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(style_figure(px.scatter(filtered.sample(min(5000, len(filtered)), random_state=42), x="temp", y="cnt", color="season_name", opacity=.45, title="Temperature and demand", labels={"temp": "Normalized temperature", "cnt": "Hourly rentals"}), 370), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(style_figure(px.scatter(filtered.sample(min(5000, len(filtered)), random_state=42), x="hum", y="cnt", color="weather_name", opacity=.45, title="Humidity and demand", labels={"hum": "Normalized humidity", "cnt": "Hourly rentals"}), 370), use_container_width=True, config={"displayModeBar": False})
    weather_means = filtered.groupby("weather_name", as_index=False)["cnt"].mean()
    st.plotly_chart(style_figure(px.bar(weather_means, x="weather_name", y="cnt", color="weather_name", title="Weather impact", labels={"weather_name": "Weather", "cnt": "Mean rentals"}), 350), use_container_width=True, config={"displayModeBar": False})
    numeric = filtered[["season", "mnth", "hr", "holiday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed", "cnt"]].corr()
    st.plotly_chart(heatmap(numeric, "Filtered correlation heatmap"), use_container_width=True, config={"displayModeBar": False})
