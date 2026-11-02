"""Dashboard design tokens and Streamlit overrides."""

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500;600;700&display=swap');
        :root {
            --bg: #0b1120;
            --surface: #121b2e;
            --surface-2: #17233a;
            --border: rgba(148, 163, 184, .16);
            --text: #f8fafc;
            --muted: #91a0b7;
            --accent: #22c55e;
            --blue: #60a5fa;
            --amber: #fbbf24;
        }
        html, body, [class*="css"] { font-family: 'Fira Sans', sans-serif; }
        .stApp { background: var(--bg); color: var(--text); }
        [data-testid="stHeader"] { background: rgba(11, 17, 32, .88); }
        [data-testid="stSidebar"] { background: #0e1728; border-right: 1px solid var(--border); }
        [data-testid="stSidebar"] > div:first-child { padding: 2rem 1.15rem; }
        .block-container { max-width: 1440px; padding: 2.5rem 3.2rem 4rem; }
        .brand-lockup { display:flex; gap:.75rem; align-items:center; }
        .brand-mark { width:36px; height:36px; display:grid; place-items:center; border-radius:11px; background:var(--accent); color:#07110a; font:600 1.2rem 'Fira Code'; box-shadow:0 10px 24px rgba(34,197,94,.22); }
        .brand-name { color:var(--text); font-size:1.04rem; font-weight:600; letter-spacing:-.02em; }
        .brand-subtitle { color:var(--accent); font:500 .72rem 'Fira Code'; letter-spacing:.12em; text-transform:uppercase; }
        .sidebar-rule { height:1px; background:var(--border); margin:1.6rem 0 1.4rem; }
        [data-testid="stSidebar"] .stRadio label { color:#b8c4d7; }
        [data-testid="stSidebar"] .stRadio > div { gap:.28rem; }
        [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] { padding:.64rem .72rem; border-radius:8px; }
        [data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:has(input:checked) { background:rgba(34,197,94,.12); }
        [data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:has(input:checked) label { color:#f8fafc; }
        .sidebar-status { display:flex; align-items:center; gap:.5rem; color:#d5deeb; font-size:.8rem; margin-top:2rem; }
        .sidebar-meta { color:#70809a; font-size:.72rem; line-height:1.65; margin-top:.7rem; }
        .status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#64748b; }
        .status-dot.online { background:var(--accent); box-shadow:0 0 0 4px rgba(34,197,94,.12); }
        .status-dot.warning { background:var(--amber); }
        .app-header { display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; padding:.3rem 0 2rem; }
        .eyebrow { color:var(--accent); font:500 .68rem 'Fira Code'; letter-spacing:.14em; }
        h1 { margin:.55rem 0 .45rem; color:var(--text); font-size:2rem; letter-spacing:-.04em; font-weight:600; }
        .app-header p { color:var(--muted); margin:0; font-size:.96rem; }
        .header-chip { border:1px solid var(--border); background:rgba(18,27,46,.7); border-radius:999px; padding:.55rem .8rem; color:#c7d2e3; font:500 .74rem 'Fira Code'; white-space:nowrap; }
        .header-chip .status-dot { margin-right:.45rem; vertical-align:middle; }
        .section-kicker { color:var(--muted); font:500 .69rem 'Fira Code'; letter-spacing:.12em; text-transform:uppercase; margin:1.2rem 0 .7rem; }
        .section-title { color:var(--text); font-size:1.25rem; font-weight:600; letter-spacing:-.025em; margin:0 0 .2rem; }
        .section-description { color:var(--muted); font-size:.86rem; margin:0 0 1rem; }
        .metric-card { background:linear-gradient(145deg, rgba(23,35,58,.92), rgba(18,27,46,.92)); border:1px solid var(--border); border-radius:13px; padding:1.05rem 1.15rem; min-height:112px; box-shadow:0 12px 30px rgba(0,0,0,.12); }
        .metric-label { color:var(--muted); font:500 .68rem 'Fira Code'; letter-spacing:.09em; text-transform:uppercase; }
        .metric-value { color:var(--text); font:600 1.7rem 'Fira Code'; margin-top:.55rem; }
        .metric-note { color:#71819b; font-size:.74rem; margin-top:.22rem; }
        .panel { background:rgba(18,27,46,.74); border:1px solid var(--border); border-radius:13px; padding:1.15rem 1.2rem .8rem; }
        .insight { border-left:2px solid var(--accent); background:rgba(34,197,94,.06); border-radius:0 9px 9px 0; color:#c5d2e3; padding:.75rem .9rem; font-size:.82rem; line-height:1.5; margin:.4rem 0 1rem; }
        .prediction-panel { border:1px solid rgba(34,197,94,.32); background:linear-gradient(135deg, rgba(34,197,94,.12), rgba(18,27,46,.75)); border-radius:15px; padding:1.35rem; margin-top:1rem; }
        .prediction-number { color:#eaffef; font:600 2.7rem 'Fira Code'; letter-spacing:-.06em; }
        .prediction-label { color:#9fe6b2; font:500 .68rem 'Fira Code'; letter-spacing:.1em; text-transform:uppercase; }
        .fine-print { color:#74849d; font-size:.72rem; line-height:1.5; }
        div[data-testid="stButton"] > button { border:1px solid rgba(34,197,94,.46); background:var(--accent); color:#061109; border-radius:8px; font:600 .78rem 'Fira Code'; letter-spacing:.04em; min-height:2.7rem; transition:all .2s ease; }
        div[data-testid="stButton"] > button:hover { background:#4ade80; border-color:#4ade80; transform:translateY(-1px); box-shadow:0 9px 22px rgba(34,197,94,.18); }
        .stDownloadButton button { border-radius:8px; }
        [data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:10px; }
        @media (max-width: 900px) { .block-container { padding:1.5rem 1rem 3rem; } .app-header { display:block; } .header-chip { display:inline-block; margin-top:1rem; } h1 { font-size:1.65rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )
