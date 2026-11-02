"""Model comparison page using saved evaluation artifacts."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.charts import style_figure


def _load_metric_data(data: dict, models: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    metrics, predictions = data["metrics"].copy(), data["predictions"].copy()
    if metrics.empty or predictions.empty:
        st.error("Saved evaluation results are unavailable. Run the evaluation notebook before opening this page.")
    return metrics, predictions


def render_model_comparison(data: dict, models: dict) -> None:
    st.markdown('<div class="section-kicker">MODEL LAB</div><div class="section-title">Compare future-period performance</div><p class="section-description">Both models were tuned on 2011 and evaluated once on the unseen chronological 2012 test period.</p>', unsafe_allow_html=True)
    metrics, predictions = _load_metric_data(data, models)
    if metrics.empty:
        return
    display_names = {"random_forest": "Random Forest", "xgboost": "XGBoost"}
    metrics["display_model"] = metrics["model"].map(display_names).fillna(metrics["model"])
    cols = st.columns(4)
    for column, label in zip(cols, ["MAE", "RMSE", "R2", "MSE"]):
        with column:
            winner = metrics.loc[metrics[label].idxmax() if label == "R2" else metrics[label].idxmin(), "display_model"]
            value = metrics[label].max() if label == "R2" else metrics[label].min()
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value:,.3f}</div><div class="metric-note">best: {winner}</div></div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        metric_long = metrics.melt(id_vars="display_model", value_vars=["MAE", "RMSE"], var_name="metric", value_name="value")
        st.plotly_chart(style_figure(px.bar(metric_long, x="metric", y="value", color="display_model", barmode="group", title="Error metrics · lower is better"), 350), use_container_width=True, config={"displayModeBar": False})
    with right:
        r2 = px.bar(metrics, x="display_model", y="R2", color="display_model", title="R² score · higher is better", color_discrete_sequence=["#22c55e", "#60a5fa"])
        st.plotly_chart(style_figure(r2, 350), use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-kicker">DIAGNOSTICS</div>', unsafe_allow_html=True)
    model_choice = st.selectbox("Inspect model", list(display_names.values()))
    key = next(k for k, v in display_names.items() if v == model_choice)
    pred_col = f"{key}_prediction"
    diagnostics = predictions.copy()
    diagnostics["residual"] = diagnostics["cnt"] - diagnostics[pred_col]
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(diagnostics, x="cnt", y=pred_col, opacity=.35, title=f"Actual vs predicted · {model_choice}", labels={"cnt": "Actual rentals", pred_col: "Predicted rentals"})
        min_v, max_v = diagnostics[["cnt", pred_col]].min().min(), diagnostics[["cnt", pred_col]].max().max()
        fig.add_shape(type="line", x0=min_v, y0=min_v, x1=max_v, y1=max_v, line={"color": "#22c55e", "dash": "dash"})
        st.plotly_chart(style_figure(fig), use_container_width=True, config={"displayModeBar": False})
    with c2:
        fig = px.histogram(diagnostics, x="residual", nbins=45, marginal="box", title=f"Residual distribution · {model_choice}", labels={"residual": "Actual − predicted"})
        st.plotly_chart(style_figure(fig), use_container_width=True, config={"displayModeBar": False})
    fig = px.scatter(diagnostics, x=pred_col, y="residual", opacity=.35, title=f"Residuals vs predicted · {model_choice}", labels={pred_col: "Predicted rentals", "residual": "Residual"})
    fig.add_hline(y=0, line_dash="dash", line_color="#22c55e")
    st.plotly_chart(style_figure(fig), use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-kicker">INTERPRETABILITY</div>', unsafe_allow_html=True)
    importance_frames = []
    for name, frame in data["importances"].items():
        copy = frame.head(10).copy()
        copy["display_model"] = display_names.get(name, name)
        importance_frames.append(copy)
    if importance_frames:
        importance = pd.concat(importance_frames, ignore_index=True)
        fig = px.bar(importance, x="importance", y="feature", color="display_model", orientation="h", facet_col="display_model", title="Top transformed feature importances")
        fig.update_yaxes(matches=None)
        st.plotly_chart(style_figure(fig, 520), use_container_width=True, config={"displayModeBar": False})
    st.dataframe(metrics[["display_model", "MAE", "MSE", "RMSE", "R2"]].rename(columns={"display_model": "Model"}).set_index("Model").style.format("{:.3f}"), use_container_width=True)
    st.caption("Metric winners are selected from the saved evaluation CSV. Feature importance is model-specific association, not causal evidence.")
