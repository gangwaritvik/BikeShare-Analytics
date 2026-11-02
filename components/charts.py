"""Plotly chart helpers with the dashboard visual language."""

import plotly.express as px
import plotly.graph_objects as go


BG = "rgba(0,0,0,0)"
GRID = "rgba(148,163,184,.12)"
TEXT = "#c8d3e2"
GREEN = "#22c55e"
BLUE = "#60a5fa"
AMBER = "#fbbf24"


def style_figure(fig, height: int = 360):
    fig.update_layout(
        height=height,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font={"family": "Fira Sans, sans-serif", "color": TEXT, "size": 12},
        margin={"l": 8, "r": 8, "t": 35, "b": 8},
        legend={"bgcolor": "rgba(0,0,0,0)", "orientation": "h", "y": 1.12},
        hoverlabel={"bgcolor": "#17233a", "font": {"color": "#f8fafc"}},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return fig


def line_chart(data, x, y, color=None, title=""):
    return style_figure(px.line(data, x=x, y=y, color=color, markers=True, title=title))


def bar_chart(data, x, y, color=None, title=""):
    return style_figure(px.bar(data, x=x, y=y, color=color, title=title), 340)


def box_chart(data, x, y, title=""):
    return style_figure(px.box(data, x=x, y=y, points=False, title=title), 340)


def scatter_chart(data, x, y, color=None, title=""):
    return style_figure(px.scatter(data, x=x, y=y, color=color, opacity=.55, title=title), 360)


def heatmap(correlation, title="Correlation matrix"):
    fig = go.Figure(go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.index,
        zmin=-1,
        zmax=1,
        colorscale=[[0, "#2563eb"], [.5, "#17233a"], [1, "#22c55e"]],
        colorbar={"title": "r", "tickfont": {"color": TEXT}},
        hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>",
    ))
    return style_figure(fig, 520).update_layout(title=title)
