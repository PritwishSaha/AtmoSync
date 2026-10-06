import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

st.set_page_config(
    page_title="AtmoSync Monitoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PALETTE AND PLOTLY THEME  (cold-chain: deep teal ink, frost, amber)
# ============================================================
COLORS = {
    "bg": "#0A1B21", "card": "#10262E", "card2": "#143039", "border": "#1F3F4A",
    "primary": "#34D399", "accent": "#7DD3FC", "warning": "#FBBF24",
    "danger": "#FB7185", "muted": "#8FA9B3", "text": "#E8F1F4",
}
CATEGORICAL_SEQ = ["#7DD3FC", "#34D399", "#FBBF24", "#C4B5FD",
                   "#F9A8D4", "#FB923C", "#5EEAD4", "#FDE68A"]
RISK_ORDER = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
RISK_COLOR_MAP = {"LOW": "#34D399", "MEDIUM": "#FBBF24", "HIGH": "#FB923C", "CRITICAL": "#E11D48"}
CONDITION_COLOR_MAP = {"NORMAL": "#34D399", "ANOMALY": "#FB7185"}
RATE_SCALE = ["#34D399", "#FBBF24", "#FB7185"]

tpl = go.layout.Template(pio.templates["plotly_dark"])
tpl.layout.update(
    paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"],
    font=dict(color=COLORS["text"], family="DM Sans, sans-serif", size=13),
    title=dict(font=dict(size=16, family="Bricolage Grotesque, sans-serif"), x=0.02),
    colorway=CATEGORICAL_SEQ,
    margin=dict(t=60, l=16, r=16, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    hoverlabel=dict(bgcolor=COLORS["card2"], bordercolor=COLORS["border"], font_size=13),
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], title=None),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], title=None),
)
pio.templates["atmosync"] = tpl
pio.templates.default = "atmosync"

# ============================================================
# CSS
# ============================================================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=DM+Sans:wght@400;500;700&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background: radial-gradient(1100px 500px at 10% -10%, #123340 0%, {COLORS["bg"]} 60%); }}
header[data-testid="stHeader"] {{ background: transparent; }}
footer, #MainMenu {{ visibility: hidden; }}
section[data-testid="stSidebar"] {{ background: {COLORS["card"]}; border-right: 1px solid {COLORS["border"]}; }}

.hero {{ display:grid; grid-template-columns: 1fr auto; gap:2rem; align-items:end;
  padding:2rem 2.2rem; border-radius:20px; margin-bottom:1.4rem;
  background: linear-gradient(120deg, #0F3A44 0%, {COLORS["card"]} 65%);
  border:1px solid {COLORS["border"]}; }}
.hero h1 {{ margin:0; font-family:'Bricolage Grotesque',sans-serif; font-weight:800;
  font-size:clamp(2rem,4vw,3rem); letter-spacing:-1px; color:{COLORS["text"]}; }}
.hero p {{ margin:.5rem 0 0; color:{COLORS["muted"]}; max-width:620px; line-height:1.55; }}
.hero .meta {{ margin-top:1rem; color:{COLORS["accent"]}; font-size:.88rem; font-weight:500; }}
.hero-stat {{ text-align:right; }}
.hero-stat .big {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:clamp(2.8rem,6vw,4.6rem);
  line-height:1; color:{COLORS["danger"]}; letter-spacing:-2px; }}
.hero-stat .cap {{ color:{COLORS["muted"]}; font-size:.9rem; max-width:240px; margin-left:auto; margin-top:.4rem; }}
@media (max-width:760px) {{ .hero {{ grid-template-columns:1fr; }} .hero-stat, .hero-stat .cap {{ text-align:left; margin-left:0; }} }}

.kpi {{ position:relative; overflow:hidden; height:100%; background:{COLORS["card"]};
  border:1px solid {COLORS["border"]}; border-radius:14px; padding:1rem 1.1rem;
  background-image: radial-gradient(circle at 100% 0%, color-mix(in srgb, var(--accent) 20%, transparent), transparent 55%);
  transition: border-color .2s ease; }}
.kpi:hover {{ border-color: var(--accent); }}
.kpi-label {{ color:{COLORS["muted"]}; font-size:.85rem; font-weight:500; }}
.kpi-value {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.9rem;
  color:{COLORS["text"]}; margin:.2rem 0 .1rem; letter-spacing:-.5px; }}
.kpi-sub {{ color:var(--accent); font-size:.8rem; font-weight:500; }}

button[data-baseweb="tab"] {{ font-weight:600; color:{COLORS["muted"]}; padding:.6rem 1rem; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color:{COLORS["text"]}; }}
div[data-baseweb="tab-highlight"] {{ background:{COLORS["primary"]}; height:3px; }}
div[data-baseweb="tab-border"] {{ background:{COLORS["border"]}; }}

div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] {{
  background:{COLORS["card"]}; border:1px solid {COLORS["border"]}; border-radius:14px; padding:.5rem; }}
.panel-title {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.3rem;
  margin:1.2rem 0 .2rem; color:{COLORS["text"]}; }}
.panel-note {{ color:{COLORS["muted"]}; font-size:.92rem; margin-bottom:.8rem; }}
.pill {{ display:inline-block; padding:5px 14px; border-radius:999px; font-weight:600; font-size:.88rem;
  color:{COLORS["danger"]}; background:rgba(251,113,133,.12); border:1px solid rgba(251,113,133,.35); margin-bottom:.7rem; }}
hr {{ border-color:{COLORS["border"]} !important; }}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================
def panel(title: str, note: str = ""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-note">{note}</div>',
                unsafe_allow_html=True)

def kpi(label, value, sub, color):
    return (f'<div class="kpi" style="--accent:{color}"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>')

def show(fig, height=380):
    fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True)

def table(df, **kwargs):
    st.dataframe(df, use_container_width=True, hide_index=True, **kwargs)

def pct(a, b):
    return a / b * 100 if b else 0.0

def hex_rgba(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"

def counts(series, name):
    return series.value_counts().rename_axis(name).reset_index(name="count")

def bucket_freq(ts):
    span = ts.max() - ts.min()
    return "10min" if span <= pd.Timedelta(days=1) else "60min" if span <= pd.Timedelta(days=7) else "D"

def donut(df, names, cmap, title, center):
    fig = px.pie(df, names=names, values="count", hole=0.62, title=title,
                 color=names, color_discrete_map=cmap)
    fig.update_traces(textinfo="percent", sort=False,
                      marker=dict(line=dict(color=COLORS["card"], width=3)))
    fig.add_annotation(text=center, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=24, family="Bricolage Grotesque, sans-serif"))
    fig.update_layout(legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"))
    return fig

def hbar(df, cat, title, cmap=None):
    fig = px.bar(df.sort_values("count"), x="count", y=cat, orientation="h", text="count",
                 title=title, color=cat, color_discrete_map=cmap)
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False)
    return fig

def band_chart(df, col, color, title, freq):
    g = df.groupby(df["timestamp"].dt.floor(freq))[col].agg(["mean", "min", "max"]).reset_index()
    fig = go.Figure()
    fig.add_scatter(x=g["timestamp"], y=g["max"], mode="lines", line=dict(width=0),
                    hoverinfo="skip", showlegend=False)
    fig.add_scatter(x=g["timestamp"], y=g["min"], mode="lines", line=dict(width=0), fill="tonexty",
                    fillcolor=hex_rgba(color, 0.16), hoverinfo="skip", showlegend=False)
    fig.add_scatter(x=g["timestamp"], y=g["mean"], mode="lines", name="Mean",
                    line=dict(color=color, width=2.5), hovertemplate="%{y:.2f}<extra>Mean</extra>")
    fig.update_layout(title=title, showlegend=False, hovermode="x unified")
    return fig

def summarize(df, key):
    s = (df.groupby(key)
           .agg(total_records=("is_anomaly", "size"), anomalies=("is_anomaly", "sum"))
           .reset_index())
    s["anomaly_rate"] = s["anomalies"] / s["total_records"] * 100
    return s.sort_values("anomaly_rate", ascending=False)

def rate_bar(s, key, title):
    fig = px.bar(s, x=key, y="anomaly_rate", title=title, text_auto=".1f",
                 color="anomaly_rate", color_continuous_scale=RATE_SCALE)
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(type="category")
    fig.update_yaxes(title="Anomaly rate (%)")
    fig.update_layout(coloraxis_showscale=False)
    return fig

RATE_COL = st.column_config.ProgressColumn("Anomaly rate", format="%.1f%%", min_value=0, max_value=100)

# ============================================================
# LOAD DATA
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

@st.cache_data
def load_data():
    monitoring = pd.read_csv(PROCESSED_DIR / "prediction_monitoring.csv")
    telemetry = pd.read_csv(PROCESSED_DIR / "iot_telemetry_features.csv")
    arbitrage = pd.read_csv(PROCESSED_DIR / "arbitrage_decisions.csv")
    for df in (monitoring, telemetry, arbitrage):
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return monitoring, telemetry, arbitrage

try:
    monitoring_raw, telemetry_raw, arbitrage_raw = load_data()
except FileNotFoundError as e:
    st.error(f"Data file not found: {e.filename}. Run the data pipeline first, then reload.")
    st.stop()

# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown("### Filters")
    sel_c = st.multiselect("Container", sorted(monitoring_raw["container_id"].unique()),
                           placeholder="All containers")
    sel_m = st.multiselect("Commodity", sorted(monitoring_raw["commodity"].unique()),
                           placeholder="All commodities")
    dmin = min(monitoring_raw["timestamp"].min(), telemetry_raw["timestamp"].min()).date()
    dmax = max(monitoring_raw["timestamp"].max(), telemetry_raw["timestamp"].max()).date()
    dr = st.date_input("Date range", value=(dmin, dmax), min_value=dmin, max_value=dmax)
    d0, d1 = (dr if isinstance(dr, (tuple, list)) and len(dr) == 2 else (dmin, dmax))
    st.caption("Leave a filter empty to include everything.")

def apply_filters(df):
    out = df
    if sel_c and "container_id" in out:
        out = out[out["container_id"].isin(sel_c)]
    if sel_m and "commodity" in out:
        out = out[out["commodity"].isin(sel_m)]
    d = out["timestamp"].dt.date
    return out[(d >= d0) & (d <= d1)].copy()

m = apply_filters(monitoring_raw)
t = apply_filters(telemetry_raw)
a = apply_filters(arbitrage_raw)

if m.empty:
    st.warning("No records match these filters. Widen the date range or clear a container or commodity filter.")
    st.stop()

m["is_anomaly"] = (m["predicted_condition"] == "ANOMALY").astype(int)

# ============================================================
# KPI CALCULATIONS
# ============================================================
total_records = len(m)
predicted_anomalies = int(m["is_anomaly"].sum())
high_risk_records = int(t["spoilage_risk"].isin(["HIGH", "CRITICAL"]).sum())
arb_flag = a["arbitrage_opportunity"].astype(str).str.strip().str.lower().eq("true")
arbitrage_opportunities = int(arb_flag.sum())
average_risk = t["environmental_risk_score"].mean() if len(t) else 0.0
average_confidence = m["prediction_confidence"].mean()
container_rates = summarize(m, "container_id")
worst = container_rates.iloc[0]

# ============================================================
# HERO
# ============================================================
st.markdown(
    f"""
<div class="hero">
  <div>
    <h1>AtmoSync</h1>
    <p>Micro-climate analytics for simulated IoT telemetry: environmental risk, ML predictions,
    container health, and spoilage-arbitrage decisions in one view.</p>
    <div class="meta">{total_records:,} records from {d0:%d %b %Y} to {d1:%d %b %Y}</div>
  </div>
  <div class="hero-stat">
    <div class="big">{worst["anomaly_rate"]:.1f}%</div>
    <div class="cap">Container {worst["container_id"]} has the highest predicted anomaly rate</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# KPI CARDS
# ============================================================
cards = [
    ("Telemetry records", f"{total_records:,}", "in current selection", COLORS["accent"]),
    ("Predicted anomalies", f"{predicted_anomalies:,}", f"{pct(predicted_anomalies, total_records):.1f}% of records", COLORS["danger"]),
    ("High or critical risk", f"{high_risk_records:,}", f"{pct(high_risk_records, len(t)):.1f}% of telemetry", COLORS["warning"]),
    ("Arbitrage opportunities", f"{arbitrage_opportunities:,}", f"of {len(a):,} decisions", COLORS["primary"]),
    ("Avg environmental risk", f"{average_risk:.2f}", f"peak {t['environmental_risk_score'].max():.2f}" if len(t) else "no data", "#C4B5FD"),
    ("Avg ML confidence", f"{average_confidence:.3f}", f"median {m['prediction_confidence'].median():.3f}", COLORS["accent"]),
]
for col, c in zip(st.columns(6), cards):
    col.markdown(kpi(*c), unsafe_allow_html=True)

st.write("")

# ============================================================
# TABS
# ============================================================
tab_over, tab_sensor, tab_ml, tab_assets, tab_arb, tab_risk = st.tabs(
    ["Overview", "Sensors", "ML monitoring", "Containers and commodities", "Arbitrage", "High-risk telemetry"]
)

# ---------- Overview ----------
with tab_over:
    c1, c2 = st.columns(2)
    with c1:
        show(donut(counts(m["predicted_condition"], "condition"), "condition", CONDITION_COLOR_MAP,
                   "Predicted condition", f"{pct(predicted_anomalies, total_records):.1f}%"), 360)
    with c2:
        rc = counts(t["spoilage_risk"], "risk").set_index("risk").reindex(RISK_ORDER, fill_value=0).reset_index()
        rc = rc[rc["count"] > 0]
        show(donut(rc, "risk", RISK_COLOR_MAP, "Spoilage risk",
                   f"{pct(high_risk_records, len(t)):.0f}% high"), 360)

    freq = bucket_freq(m["timestamp"])
    trend = m.groupby(m["timestamp"].dt.floor(freq))["is_anomaly"].sum().reset_index()
    fig = go.Figure(go.Scatter(x=trend["timestamp"], y=trend["is_anomaly"], mode="lines", fill="tozeroy",
                               line=dict(color=COLORS["danger"], width=2.5),
                               fillcolor=hex_rgba(COLORS["danger"], 0.15),
                               hovertemplate="%{y} anomalies<extra></extra>"))
    fig.update_layout(title="Predicted anomalies over time", hovermode="x unified")
    show(fig, 320)

# ---------- Sensors ----------
with tab_sensor:
    panel("Sensor trends", "The line is the average per time bucket; the shaded band spans the min to max reading.")
    if t.empty:
        st.info("No telemetry in this selection.")
    else:
        freq = bucket_freq(t["timestamp"])
        specs = [("temperature", COLORS["danger"], "Temperature"),
                 ("humidity", COLORS["accent"], "Humidity"),
                 ("vibration", COLORS["warning"], "Vibration")]
        for col, (key, color, title) in zip(st.columns(3), specs):
            with col:
                show(band_chart(t, key, color, title, freq), 330)
                st.caption(f"min {t[key].min():.1f}  |  avg {t[key].mean():.1f}  |  max {t[key].max():.1f}")

# ---------- ML monitoring ----------
with tab_ml:
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.histogram(m, x="prediction_confidence", nbins=30, title="Prediction confidence distribution",
                           color_discrete_sequence=[COLORS["accent"]])
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=0.05)
        show(fig, 340)
    with c2:
        g = go.Figure(go.Indicator(
            mode="gauge+number", value=average_confidence,
            number=dict(valueformat=".3f", font=dict(size=40, family="Bricolage Grotesque, sans-serif")),
            title=dict(text="Average confidence"),
            gauge=dict(axis=dict(range=[0, max(1, average_confidence)]), bar=dict(color=COLORS["primary"]),
                       bgcolor=COLORS["card2"], borderwidth=0)))
        show(g, 340)
    c1, c2 = st.columns(2)
    with c1:
        show(hbar(counts(m["confidence_category"], "confidence"), "confidence", "Confidence categories"), 320)
    with c2:
        show(hbar(counts(m["monitoring_level"], "monitoring_level"), "monitoring_level", "Monitoring levels"), 320)

# ---------- Containers and commodities ----------
with tab_assets:
    if m["container_id"].nunique() > 1 and m["commodity"].nunique() > 1:
        pv = m.pivot_table(index="container_id", columns="commodity", values="is_anomaly", aggfunc="mean") * 100
        fig = px.imshow(pv, text_auto=".0f", aspect="auto", color_continuous_scale=RATE_SCALE,
                        title="Anomaly rate (%) by container and commodity")
        fig.update_layout(coloraxis_colorbar=dict(thickness=10, title=None))
        show(fig, 420)

    commodity_rates = summarize(m, "commodity")
    c1, c2 = st.columns(2)
    with c1:
        show(rate_bar(container_rates, "container_id", "Anomaly rate by container"), 340)
        table(container_rates, column_config={"anomaly_rate": RATE_COL})
    with c2:
        show(rate_bar(commodity_rates, "commodity", "Anomaly rate by commodity"), 340)
        table(commodity_rates, column_config={"anomaly_rate": RATE_COL})

# ---------- Arbitrage ----------
with tab_arb:
    if a.empty:
        st.info("No arbitrage decisions in this selection.")
    else:
        c1, c2 = st.columns([3, 2])
        with c1:
            show(hbar(counts(a["recommended_action"], "recommended_action"),
                      "recommended_action", "Recommended operational actions"), 360)
        with c2:
            opp = pd.DataFrame({"outcome": ["Opportunity", "No opportunity"],
                                "count": [arbitrage_opportunities, len(a) - arbitrage_opportunities]})
            show(donut(opp, "outcome", {"Opportunity": COLORS["primary"], "No opportunity": COLORS["border"]},
                       "Arbitrage opportunities", f"{pct(arbitrage_opportunities, len(a)):.0f}%"), 360)
        panel("Latest decisions", "Showing the 500 most recent rows.")
        table(a.sort_values("timestamp", ascending=False).head(500))

# ---------- High-risk telemetry ----------
with tab_risk:
    hr = t[t["spoilage_risk"].isin(["HIGH", "CRITICAL"])].copy()
    if len(t):
        sample = t.sample(min(len(t), 3000), random_state=1)
        fig = px.scatter(sample, x="temperature", y="humidity", color="spoilage_risk", opacity=0.7,
                         category_orders={"spoilage_risk": RISK_ORDER}, color_discrete_map=RISK_COLOR_MAP,
                         title="Temperature vs humidity by spoilage risk")
        fig.update_layout(legend_title_text="")
        show(fig, 380)

    st.markdown(f'<span class="pill">{len(hr):,} high or critical risk records</span>', unsafe_allow_html=True)
    if hr.empty:
        st.success("No high or critical risk records in this selection.")
    else:
        cols = ["container_id", "timestamp", "commodity", "temperature", "humidity",
                "vibration", "environmental_risk_score", "spoilage_risk"]
        view = hr[cols].sort_values("environmental_risk_score", ascending=False)
        st.download_button("Download as CSV", view.to_csv(index=False).encode("utf-8"),
                           file_name="high_risk_telemetry.csv", mime="text/csv")
        styler = view.style
        color_fn = getattr(styler, "map", None) or styler.applymap
        styled = color_fn(lambda v: f"color: {RISK_COLOR_MAP.get(v, COLORS['text'])}; font-weight:700;",
                          subset=["spoilage_risk"])
        table(styled, column_config={
            "environmental_risk_score": st.column_config.ProgressColumn(
                "Risk score", format="%.2f", min_value=0, max_value=float(t["environmental_risk_score"].max()))})

st.divider()
st.markdown(
    f'<p style="text-align:center;color:{COLORS["muted"]};font-size:.85rem;">'
    "AtmoSync micro-climate arbitrage analytics. Based on simulated telemetry data.</p>",
    unsafe_allow_html=True,
)