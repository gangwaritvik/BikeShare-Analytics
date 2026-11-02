"""Streamlit entry point for the BikeShare Analytics dashboard."""

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from components.styles import inject_styles
from pages.data_insights import render_data_insights
from pages.demand_prediction import render_demand_prediction
from pages.model_comparison import render_model_comparison
from pages.overview import render_overview
from utils.data_loader import load_dashboard_data
from utils.model_loader import load_models, model_status


st.set_page_config(
    page_title="BikeShare Analytics",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()


@st.cache_data(show_spinner=False)
def get_data():
    return load_dashboard_data(ROOT)


@st.cache_resource(show_spinner=False)
def get_models():
    return load_models(ROOT)


data = get_data()
models, model_errors = get_models()
status_text, status_class = model_status(models, model_errors)

with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark">B</div>
            <div>
                <div class="brand-name">BikeShare</div>
                <div class="brand-subtitle">Analytics</div>
            </div>
        </div>
        <div class="sidebar-rule"></div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("INTELLIGENT DEMAND FORECASTING")
    page = st.radio(
        "Workspace",
        ["Overview", "Demand Prediction", "Model Comparison", "Data Insights"],
        label_visibility="collapsed",
    )
    st.markdown(
        f"""
        <div class="sidebar-status">
            <span class="status-dot {status_class}"></span>
            <span>{status_text}</span>
        </div>
        <div class="sidebar-meta">UCI Bike Sharing Dataset<br>Hourly observations · 2011–2012</div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="app-header">
        <div>
            <div class="eyebrow">BIKESHARE ANALYTICS / COMMAND CENTER</div>
            <h1>Intelligent Bike Rental Demand Forecasting</h1>
            <p>Explore demand patterns, compare trained models, and generate leakage-safe hourly forecasts.</p>
        </div>
        <div class="header-chip"><span class="status-dot online"></span> Live model workspace</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if model_errors:
    st.warning("Some model artifacts could not be loaded. Prediction and comparison features may be limited.")

if page == "Overview":
    render_overview(data)
elif page == "Demand Prediction":
    render_demand_prediction(data, models)
elif page == "Model Comparison":
    render_model_comparison(data, models)
else:
    render_data_insights(data)
