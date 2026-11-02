"""Overview dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.charts import bar_chart, box_chart, line_chart, style_figure


def _metric(label, value, note):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def render_overview(data: dict) -> None:
    raw = data["raw"]
    hourly = raw.groupby("hr", as_index=False)["cnt"].mean()
    monthly = raw.assign(month_name=raw["dteday"].dt.strftime("%b")).groupby(
        ["year", "mnth", "month_name"], as_index=False
    )["cnt"].mean()
    season = raw.groupby("season_name", as_index=False)["cnt"].mean()
    work = raw.assign(work_status=raw["workingday"].map({0: "Non-working day", 1: "Working day"}))
    work = work.groupby("work_status", as_index=False)["cnt"].mean()
    weather = raw.groupby("weather_name", as_index=False)["cnt"].mean()

    st.markdown('<div class="section-kicker">OPERATIONS SNAPSHOT</div><div class="section-title">Demand at a glance</div><p class="section-description">A measured view of 17,379 hourly observations from Washington D.C. bike-sharing activity.</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        _metric("Total rentals", f"{raw['cnt'].sum():,.0f}", "all recorded hours")
    with cols[1]:
        _metric("Average / hour", f"{raw['cnt'].mean():,.1f}", "rental count")
    with cols[2]:
        _metric("Peak hour", f"{int(hourly.loc[hourly['cnt'].idxmax(), 'hr']):02d}:00", f"{hourly['cnt'].max():,.1f} avg rentals")
    with cols[3]:
        _metric("Highest season", season.loc[season['cnt'].idxmax(), 'season_name'], f"{season['cnt'].max():,.1f} avg rentals")

    st.markdown('<div class="section-kicker">DEMAND RHYTHM</div>', unsafe_allow_html=True)
    left, right = st.columns([1.45, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.plotly_chart(line_chart(hourly, "hr", "cnt", title="Hourly rental demand"), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f'<div class="insight">Demand concentrates around the commute window: the strongest observed average is {int(hourly.loc[hourly["cnt"].idxmax(), "hr"]):02d}:00, with a second high point at {int(hourly.nlargest(2, "cnt").iloc[-1]["hr"]):02d}:00.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.plotly_chart(box_chart(raw, "season_name", "cnt", "Seasonal demand distribution"), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="insight">Season affects the demand baseline. Fall has the highest observed seasonal mean, while spring is the lowest.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">CONTEXT SIGNALS</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(line_chart(monthly, "mnth", "cnt", "year", "Monthly demand trend"), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(bar_chart(work, "work_status", "cnt", title="Working day vs non-working day"), use_container_width=True, config={"displayModeBar": False})
    with c3:
        st.plotly_chart(bar_chart(weather, "weather_name", "cnt", title="Weather vs rental demand"), use_container_width=True, config={"displayModeBar": False})
    st.caption("Charts are calculated from the original dataset. Counts are descriptive averages, not causal estimates.")
