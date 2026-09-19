import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AtmoSync Monitoring Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# COLOR PALETTE & PLOTLY THEME
# ============================================================

COLORS = {
    "bg": "#0E1117",
    "card": "#161B22",
    "card_border": "#232A34",
    "primary": "#22C55E",
    "primary_dark": "#15803D",
    "accent": "#38BDF8",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "muted": "#9CA3AF",
    "text": "#F3F4F6",
}

CATEGORICAL_SEQ = [
    "#22C55E", "#38BDF8", "#F59E0B", "#A78BFA",
    "#F472B6", "#F87171", "#2DD4BF", "#FACC15",
]

RISK_COLOR_MAP = {
    "LOW": "#22C55E",
    "MEDIUM": "#FACC15",
    "HIGH": "#F59E0B",
    "CRITICAL": "#EF4444",
}

CONDITION_COLOR_MAP = {
    "NORMAL": "#22C55E",
    "ANOMALY": "#EF4444",
}

pio.templates["atmosync"] = pio.templates["plotly_dark"]
pio.templates["atmosync"].layout.update(
    paper_bgcolor=COLORS["card"],
    plot_bgcolor=COLORS["card"],
    font=dict(color=COLORS["text"], family="Inter, -apple-system, sans-serif", size=13),
    title=dict(font=dict(size=16, color=COLORS["text"])),
    colorway=CATEGORICAL_SEQ,
    margin=dict(t=60, l=10, r=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(gridcolor=COLORS["card_border"], zerolinecolor=COLORS["card_border"]),
    yaxis=dict(gridcolor=COLORS["card_border"], zerolinecolor=COLORS["card_border"]),
)
pio.templates.default = "atmosync"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: radial-gradient(circle at 15% 0%, #132018 0%, {COLORS["bg"]} 45%);
    }}

    /* Hero banner */
    .hero-banner {{
        padding: 2rem 2.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #14532D 0%, #0E1117 70%);
        border: 1px solid {COLORS["card_border"]};
        margin-bottom: 1.6rem;
    }}
    .hero-banner h1 {{
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        color: {COLORS["text"]};
        letter-spacing: -0.5px;
    }}
    .hero-banner p {{
        margin-top: 0.4rem;
        color: {COLORS["muted"]};
        font-size: 1rem;
        max-width: 720px;
    }}
    .hero-tag {{
        display: inline-block;
        background: rgba(34,197,94,0.15);
        color: {COLORS["primary"]};
        border: 1px solid rgba(34,197,94,0.35);
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-bottom: 0.8rem;
    }}

    /* KPI cards */
    div[data-testid="stMetric"] {{
        background: {COLORS["card"]};
        border: 1px solid {COLORS["card_border"]};
        border-radius: 14px;
        padding: 1rem 1.1rem 0.8rem 1.1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        transition: border-color 0.2s ease, transform 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: {COLORS["primary"]};
        transform: translateY(-2px);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {COLORS["muted"]} !important;
        font-weight: 600;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLORS["text"]} !important;
        font-weight: 800;
        font-size: 1.7rem;
    }}

    /* Section headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.6rem 0 0.9rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid {COLORS["card_border"]};
    }}
    .section-header .num {{
        background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_dark"]});
        color: #0E1117;
        font-weight: 800;
        font-size: 0.85rem;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .section-header h3 {{
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        color: {COLORS["text"]};
    }}

    /* Chart / dataframe containers */
    div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] {{
        background: {COLORS["card"]};
        border: 1px solid {COLORS["card_border"]};
        border-radius: 14px;
        padding: 0.6rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
    }}

    hr {{
        border-color: {COLORS["card_border"]} !important;
    }}

    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True
)


def section_header(number: str, title: str):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="num">{number}</div>
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    monitoring = pd.read_csv(
        PROCESSED_DIR / "prediction_monitoring.csv"
    )

    telemetry = pd.read_csv(
        PROCESSED_DIR / "iot_telemetry_features.csv"
    )

    arbitrage = pd.read_csv(
        PROCESSED_DIR / "arbitrage_decisions.csv"
    )

    return monitoring, telemetry, arbitrage


monitoring_df, telemetry_df, arbitrage_df = load_data()


# ============================================================
# HERO / TITLE
# ============================================================

st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-tag">🌱 LIVE ANALYTICS</div>
        <h1>AtmoSync Monitoring Dashboard</h1>
        <p>
            Micro-Climate Analytics & ML Monitoring — an analytical view of
            simulated IoT telemetry, environmental risk, ML predictions,
            container-level monitoring, and spoilage-arbitrage decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA PREPARATION
# ============================================================

monitoring_df["timestamp"] = pd.to_datetime(
    monitoring_df["timestamp"]
)

telemetry_df["timestamp"] = pd.to_datetime(
    telemetry_df["timestamp"]
)

arbitrage_df["timestamp"] = pd.to_datetime(
    arbitrage_df["timestamp"]
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_records = len(monitoring_df)

predicted_anomalies = (
    monitoring_df["predicted_condition"]
    .eq("ANOMALY")
    .sum()
)

high_risk_records = (
    telemetry_df["spoilage_risk"]
    .isin(["HIGH", "CRITICAL"])
    .sum()
)

arbitrage_opportunities = (
    arbitrage_df["arbitrage_opportunity"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("true")
    .sum()
)

average_risk = telemetry_df[
    "environmental_risk_score"
].mean()

average_confidence = monitoring_df[
    "prediction_confidence"
].mean()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "📡 Telemetry Records",
    f"{total_records:,}"
)

col2.metric(
    "⚠️ Predicted Anomalies",
    f"{predicted_anomalies:,}"
)

col3.metric(
    "🔥 High/Critical Risk",
    f"{high_risk_records:,}"
)

col4.metric(
    "💰 Arbitrage Opportunities",
    f"{arbitrage_opportunities:,}"
)

col5.metric(
    "📈 Avg Environmental Risk",
    f"{average_risk:.2f}"
)

col6.metric(
    "🎯 Avg ML Confidence",
    f"{average_confidence:.3f}"
)


st.divider()


# ============================================================
# SECTION 1 — CONDITION MONITORING
# ============================================================

section_header("1", "Condition Monitoring")

condition_counts = (
    monitoring_df["predicted_condition"]
    .value_counts()
    .reset_index()
)

condition_counts.columns = [
    "condition",
    "count"
]

fig_condition = px.bar(
    condition_counts,
    x="condition",
    y="count",
    title="Predicted Condition Distribution",
    text="count",
    color="condition",
    color_discrete_map=CONDITION_COLOR_MAP,
)
fig_condition.update_traces(marker_line_width=0, textposition="outside")
fig_condition.update_layout(showlegend=False)

st.plotly_chart(
    fig_condition,
    use_container_width=True
)


# ============================================================
# SECTION 2 — SENSOR ANALYTICS
# ============================================================

section_header("2", "Sensor Analytics")

col1, col2, col3 = st.columns(3)

with col1:

    fig_temp = px.line(
        telemetry_df.sort_values("timestamp"),
        x="timestamp",
        y="temperature",
        title="🌡️ Temperature Over Time",
    )
    fig_temp.update_traces(line=dict(color=COLORS["danger"], width=2))

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )


with col2:

    fig_humidity = px.line(
        telemetry_df.sort_values("timestamp"),
        x="timestamp",
        y="humidity",
        title="💧 Humidity Over Time",
    )
    fig_humidity.update_traces(line=dict(color=COLORS["accent"], width=2))

    st.plotly_chart(
        fig_humidity,
        use_container_width=True
    )


with col3:

    fig_vibration = px.line(
        telemetry_df.sort_values("timestamp"),
        x="timestamp",
        y="vibration",
        title="📳 Vibration Over Time",
    )
    fig_vibration.update_traces(line=dict(color=COLORS["warning"], width=2))

    st.plotly_chart(
        fig_vibration,
        use_container_width=True
    )


# ============================================================
# SECTION 3 — RISK ANALYTICS
# ============================================================

section_header("3", "Spoilage Risk Analytics")

risk_counts = (
    telemetry_df["spoilage_risk"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "risk",
    "count"
]

fig_risk = px.pie(
    risk_counts,
    names="risk",
    values="count",
    title="Spoilage Risk Distribution",
    color="risk",
    color_discrete_map=RISK_COLOR_MAP,
    hole=0.45,
)
fig_risk.update_traces(textinfo="percent+label", marker=dict(line=dict(color=COLORS["card"], width=2)))

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# SECTION 4 — ML MONITORING
# ============================================================

section_header("4", "ML Prediction Monitoring")

col1, col2 = st.columns(2)

with col1:

    confidence_counts = (
        monitoring_df["confidence_category"]
        .value_counts()
        .reset_index()
    )

    confidence_counts.columns = [
        "confidence",
        "count"
    ]

    fig_confidence = px.bar(
        confidence_counts,
        x="confidence",
        y="count",
        title="Prediction Confidence Categories",
        text="count",
        color="confidence",
    )
    fig_confidence.update_traces(marker_line_width=0, textposition="outside")
    fig_confidence.update_layout(showlegend=False)

    st.plotly_chart(
        fig_confidence,
        use_container_width=True
    )


with col2:

    monitoring_counts = (
        monitoring_df["monitoring_level"]
        .value_counts()
        .reset_index()
    )

    monitoring_counts.columns = [
        "monitoring_level",
        "count"
    ]

    fig_monitoring = px.bar(
        monitoring_counts,
        x="monitoring_level",
        y="count",
        title="Monitoring Levels",
        text="count",
        color="monitoring_level",
    )
    fig_monitoring.update_traces(marker_line_width=0, textposition="outside")
    fig_monitoring.update_layout(showlegend=False)

    st.plotly_chart(
        fig_monitoring,
        use_container_width=True
    )


# ============================================================
# SECTION 5 — CONTAINER ANALYSIS
# ============================================================

section_header("5", "Container-Level Analysis")

container_summary = (
    monitoring_df
    .groupby("container_id")
    .agg(
        total_records=("container_id", "size"),
        anomalies=(
            "predicted_condition",
            lambda x: (x == "ANOMALY").sum()
        )
    )
    .reset_index()
)

container_summary["anomaly_rate"] = (
    container_summary["anomalies"]
    / container_summary["total_records"]
    * 100
)

fig_container = px.bar(
    container_summary,
    x="container_id",
    y="anomaly_rate",
    title="Predicted Anomaly Rate by Container",
    text_auto=".2f",
    color="anomaly_rate",
    color_continuous_scale=["#22C55E", "#F59E0B", "#EF4444"],
)

fig_container.update_yaxes(
    title="Anomaly Rate (%)"
)
fig_container.update_layout(coloraxis_showscale=False)

st.plotly_chart(
    fig_container,
    use_container_width=True
)

st.dataframe(
    container_summary,
    use_container_width=True
)


# ============================================================
# SECTION 6 — COMMODITY ANALYSIS
# ============================================================

section_header("6", "Commodity-Level Analysis")

commodity_summary = (
    monitoring_df
    .groupby("commodity")
    .agg(
        total_records=("commodity", "size"),
        anomalies=(
            "predicted_condition",
            lambda x: (x == "ANOMALY").sum()
        )
    )
    .reset_index()
)

commodity_summary["anomaly_rate"] = (
    commodity_summary["anomalies"]
    / commodity_summary["total_records"]
    * 100
)

fig_commodity = px.bar(
    commodity_summary,
    x="commodity",
    y="anomaly_rate",
    title="Predicted Anomaly Rate by Commodity",
    text_auto=".2f",
    color="anomaly_rate",
    color_continuous_scale=["#22C55E", "#F59E0B", "#EF4444"],
)

fig_commodity.update_yaxes(
    title="Anomaly Rate (%)"
)
fig_commodity.update_layout(coloraxis_showscale=False)

st.plotly_chart(
    fig_commodity,
    use_container_width=True
)

st.dataframe(
    commodity_summary,
    use_container_width=True
)


# ============================================================
# SECTION 7 — ARBITRAGE DECISIONS
# ============================================================

section_header("7", "Spoilage Arbitrage Decisions")

action_counts = (
    arbitrage_df["recommended_action"]
    .value_counts()
    .reset_index()
)

action_counts.columns = [
    "recommended_action",
    "count"
]

fig_action = px.bar(
    action_counts,
    x="recommended_action",
    y="count",
    title="Recommended Operational Actions",
    text="count",
    color="recommended_action",
)
fig_action.update_traces(marker_line_width=0, textposition="outside")
fig_action.update_layout(showlegend=False)

st.plotly_chart(
    fig_action,
    use_container_width=True
)


# ============================================================
# SECTION 8 — HIGH-RISK RECORDS
# ============================================================

section_header("8", "High-Risk Telemetry")

high_risk_df = telemetry_df[
    telemetry_df["spoilage_risk"].isin(
        ["HIGH", "CRITICAL"]
    )
].copy()

st.markdown(
    f"""
    <div style="display:inline-block; background: rgba(239,68,68,0.12);
                border: 1px solid rgba(239,68,68,0.35); color: {COLORS['danger']};
                padding: 6px 14px; border-radius: 10px; font-weight:700; margin-bottom: 0.6rem;">
        🔥 {len(high_risk_df):,} High/Critical risk records
    </div>
    """,
    unsafe_allow_html=True
)

st.dataframe(
    high_risk_df[
        [
            "container_id",
            "timestamp",
            "commodity",
            "temperature",
            "humidity",
            "vibration",
            "environmental_risk_score",
            "spoilage_risk"
        ]
    ].sort_values(
        "environmental_risk_score",
        ascending=False
    ).style.map(
        lambda v: f"color: {RISK_COLOR_MAP.get(v, COLORS['text'])}; font-weight:700;"
        if v in RISK_COLOR_MAP else "",
        subset=["spoilage_risk"]
    ),
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    f"""
    <p style="text-align:center; color:{COLORS['muted']}; font-size:0.85rem;">
        🌱 AtmoSync · Micro-Climate Arbitrage Analytics · Dashboard based on simulated telemetry data
    </p>
    """,
    unsafe_allow_html=True
)