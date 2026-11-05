
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from datetime import datetime, timedelta


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartRouter Analytics",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PASTEL AURORA THEME
# ============================================================

BG = "#F8F6FC"
WHITE = "#FFFFFF"
INK = "#302746"
MUTED = "#786F89"
LAVENDER = "#8B76C5"
SEAFOAM = "#65B8A3"
PEACH = "#F0A982"
BLUE = "#7FA6E8"
PINK = "#D9A4C7"
SAGE = "#A9B7A0"

PALETTE = [
    LAVENDER,
    SEAFOAM,
    PEACH,
    BLUE,
    PINK,
    SAGE,
]

st.markdown(
    """
    <style>
    .stApp {
        background: #F8F6FC;
        color: #302746;
    }

    [data-testid="stHeader"] {
        background: rgba(248,246,252,0.96);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: #302746 !important;
        letter-spacing: -0.035em;
    }

    p, label, li {
        color: #403752;
    }

    [data-testid="stSidebar"] {
        background: #F0EBF8;
        border-right: 1px solid #E5DDED;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #302746;
    }

    .brand {
        font-size: 1.45rem;
        font-weight: 800;
        color: #302746;
        letter-spacing: -0.04em;
    }

    .brand-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 11px;
        margin-right: 8px;
        background: linear-gradient(135deg, #E5D9FB, #D9F3E9);
        color: #66519C;
        font-size: 1.1rem;
    }

    .sidebar-caption {
        color: #817592;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-top: 5px;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #FFFFFF 0%,
            #F0E9FC 58%,
            #E5F6F0 100%
        );
        border: 1px solid #E7DFF0;
        border-radius: 22px;
        padding: 28px 30px;
        margin-bottom: 20px;
        box-shadow: 0 5px 22px rgba(69,49,99,0.04);
    }

    .eyebrow {
        color: #8067B7;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #302746;
        font-size: clamp(1.8rem, 3vw, 2.65rem);
        font-weight: 800;
        letter-spacing: -0.055em;
        line-height: 1.15;
    }

    .hero-subtitle {
        color: #786F89;
        font-size: 0.94rem;
        line-height: 1.7;
        margin-top: 10px;
        max-width: 800px;
    }

    .section-label {
        color: #817592;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 12px 0;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E9E3F0;
        border-radius: 17px;
        padding: 16px 18px;
        min-height: 112px;
        box-shadow: 0 4px 14px rgba(69,49,99,0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #786F89 !important;
        font-size: 0.82rem;
    }

    [data-testid="stMetricValue"] {
        color: #66519C !important;
        font-size: 1.6rem;
        font-weight: 750;
    }

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid #E5DDED;
    }

    [data-testid="stTabs"] button[data-baseweb="tab"] {
        color: #716780;
        font-weight: 600;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #66519C !important;
        border-bottom-color: #8B76C5 !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background: #FFFFFF !important;
        border-color: #DED5EA !important;
        border-radius: 10px !important;
    }

    /* Keep live-router text fields readable in both light and dark browser themes. */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background: #FFFFFF !important;
        color: #302746 !important;
        -webkit-text-fill-color: #302746 !important;
        caret-color: #66519C !important;
        border: 1px solid #DED5EA !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #9288A1 !important;
        -webkit-text-fill-color: #9288A1 !important;
        opacity: 1 !important;
    }

    /* Example buttons use the secondary button style. */
    .stButton button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #49356E !important;
        border: 1px solid #D9CDEB !important;
    }

    .stButton button[kind="secondary"] *,
    .stButton button[kind="secondary"] p {
        color: #49356E !important;
        -webkit-text-fill-color: #49356E !important;
    }

    .stButton button[kind="secondary"]:hover {
        background: #F0E9FC !important;
        border-color: #BBA8DF !important;
    }

    [data-baseweb="tag"] {
        background: #E8DFF8 !important;
        border: 1px solid #D7C9EF !important;
        border-radius: 8px !important;
    }

    [data-baseweb="tag"] span {
        color: #49356E !important;
    }

    [data-testid="stTextArea"] > div > div {
        background: #FFFFFF !important;
        border-radius: 10px !important;
    }

    [data-testid="stFileUploader"] {
        background: linear-gradient(140deg, #FFFFFF, #F8F3FF);
        border: 1px dashed #BBA8DF;
        border-radius: 16px;
        padding: 12px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #F6F1FD !important;
        border: 1px dashed #C7B8E6 !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #49356E !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #8067B7 !important;
        border: none !important;
        border-radius: 9px !important;
        color: #FFFFFF !important;
    }

    [data-testid="stFileUploaderDropzone"] button * {
        color: #FFFFFF !important;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .stButton button[kind="primary"],
    .stDownloadButton button {
        background: #8067B7 !important;
        border: 1px solid #8067B7 !important;
        color: #FFFFFF !important;
    }

    .stButton button[kind="primary"] *,
    .stDownloadButton button * {
        color: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #E9E3F0;
        border-radius: 13px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #E8E1EF;
    }

    .info-card {
        background: #FFFFFF;
        border: 1px solid #E9E3F0;
        border-radius: 15px;
        padding: 17px;
        height: 100%;
    }

    .info-card-title {
        color: #786F89;
        font-size: 0.8rem;
        margin-bottom: 7px;
    }

    .info-card-value {
        color: #66519C;
        font-size: 1.45rem;
        font-weight: 800;
    }

    .info-card-description {
        color: #817592;
        font-size: 0.78rem;
        margin-top: 7px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SAMPLE DATA GENERATOR
# ============================================================

@st.cache_data
def generate_sample_data():
    """Generate realistic example request logs for testing."""

    rng = np.random.default_rng(42)
    n = 299

    timestamps = pd.date_range(
        end=pd.Timestamp.now().floor("h"),
        periods=n,
        freq="20min",
    )

    models = rng.choice(
        ["Small Model", "Large Model"],
        size=n,
        p=[0.64, 0.36],
    )

    complexities = rng.choice(
        ["Simple", "Medium", "Complex"],
        size=n,
        p=[0.43, 0.35, 0.22],
    )

    cache_hit = rng.random(n) < 0.247

    latency = []
    cost = []

    for model, complexity, hit in zip(
        models, complexities, cache_hit
    ):
        if hit:
            latency.append(
                max(25, rng.normal(115, 30))
            )
            cost.append(0.0)
        else:
            if model == "Small Model":
                base_latency = 330
                base_cost = 0.0005
            else:
                base_latency = 850
                base_cost = 0.0025

            complexity_factor = {
                "Simple": 0.75,
                "Medium": 1.0,
                "Complex": 1.65,
            }[complexity]

            latency.append(
                max(
                    40,
                    rng.normal(
                        base_latency * complexity_factor,
                        base_latency * 0.22,
                    ),
                )
            )

            cost.append(
                base_cost
                * complexity_factor
                * rng.uniform(0.75, 1.3)
            )

    example_queries = [
        "Summarize the customer feedback",
        "Explain the main findings",
        "Calculate the average sales",
        "Write a short product description",
        "Compare these two reports",
        "Analyze the quarterly results",
        "Create a detailed project plan",
        "Explain this Python error",
        "Generate a data quality summary",
        "Identify the key business trends",
    ]

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "request_id": [
                f"REQ-{i:04d}" for i in range(1, n + 1)
            ],
            "query": rng.choice(example_queries, size=n),
            "model": models,
            "complexity": complexities,
            "cache_hit": cache_hit,
            "latency_ms": np.round(latency, 1),
            "estimated_cost": np.round(cost, 7),
        }
    )


# ============================================================
# 4. NORMALIZE CSV COLUMN NAMES
# ============================================================

COLUMN_ALIASES = {
    "timestamp": [
        "timestamp", "date", "datetime", "created_at",
        "request_time", "time",
    ],
    "request_id": [
        "request_id", "id", "requestid", "request",
    ],
    "query": [
        "query", "prompt", "question", "request_text",
        "input_text",
    ],
    "model": [
        "model", "model_name", "selected_model",
        "llm", "model_used",
    ],
    "complexity": [
        "complexity", "difficulty", "task_complexity",
        "query_complexity",
    ],
    "cache_hit": [
        "cache_hit", "cache_status", "cache",
        "is_cached", "cached",
    ],
    "latency_ms": [
        "latency_ms", "latency", "response_time",
        "response_time_ms", "duration_ms",
    ],
    "estimated_cost": [
        "estimated_cost", "cost", "request_cost",
        "cost_usd", "total_cost",
    ],
}


def normalize_column_name(name):
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def normalize_dataset(raw_df):
    """Map common CSV headers to the dashboard's standard schema."""

    df = raw_df.copy()
    df.columns = [
        normalize_column_name(c) for c in df.columns
    ]

    rename_map = {}

    for standard_name, aliases in COLUMN_ALIASES.items():
        if standard_name in df.columns:
            continue

        for alias in aliases:
            normalized_alias = normalize_column_name(alias)

            if normalized_alias in df.columns:
                rename_map[normalized_alias] = standard_name
                break

    df = df.rename(columns=rename_map)

    required = [
        "model",
        "complexity",
        "latency_ms",
        "estimated_cost",
    ]

    missing = [
        col for col in required if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Your CSV is missing these required fields: "
            + ", ".join(missing)
            + ". Required fields are model, complexity, "
              "latency and estimated cost. Cache status and "
              "timestamp are also recommended."
        )

    if "timestamp" not in df.columns:
        df["timestamp"] = pd.NaT
    else:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

    if "request_id" not in df.columns:
        df["request_id"] = [
            f"REQ-{i:04d}" for i in range(1, len(df) + 1)
        ]

    if "query" not in df.columns:
        df["query"] = "(No query text provided)"

    if "cache_hit" not in df.columns:
        df["cache_hit"] = False
    else:
        if pd.api.types.is_bool_dtype(df["cache_hit"]):
            pass
        else:
            values = (
                df["cache_hit"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            df["cache_hit"] = values.isin(
                [
                    "true", "1", "yes", "y",
                    "hit", "cached", "cache hit",
                ]
            )

    df["model"] = (
        df["model"].fillna("Unknown Model").astype(str)
    )

    df["complexity"] = (
        df["complexity"].fillna("Unknown").astype(str)
    )

    df["latency_ms"] = pd.to_numeric(
        df["latency_ms"], errors="coerce"
    )

    df["estimated_cost"] = pd.to_numeric(
        df["estimated_cost"], errors="coerce"
    )

    df = df.dropna(
        subset=["latency_ms", "estimated_cost"]
    )

    df = df[
        (df["latency_ms"] >= 0)
        & (df["estimated_cost"] >= 0)
    ].copy()

    if df.empty:
        raise ValueError(
            "No valid records remain after cleaning the CSV."
        )

    return df.reset_index(drop=True)


# ============================================================
# 5. CHART HELPERS
# ============================================================

def style_chart(fig, height=360):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=55, b=15),
        font=dict(
            family="Arial, sans-serif",
            color=INK,
            size=12,
        ),
        title=dict(
            font=dict(size=15, color=INK),
            x=0.02,
            xanchor="left",
        ),
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        legend=dict(
            font=dict(color="#514660", size=11),
            bgcolor="rgba(255,255,255,0)",
        ),
        hoverlabel=dict(
            bgcolor=WHITE,
            font_color=INK,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#E5DDED",
        tickfont=dict(color="#665D75", size=11),
        title_font=dict(color="#514660"),
    )

    fig.update_yaxes(
        gridcolor="#EEE9F3",
        zeroline=False,
        tickfont=dict(color="#665D75", size=11),
        title_font=dict(color="#514660"),
    )

    return fig


def money(value):
    return f"${value:,.5f}"


# ============================================================
# 6. SIDEBAR AND DATA UPLOAD
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 8px 0 22px;">
            <div class="brand">
                <span class="brand-mark">✦</span>SmartRouter
            </div>
            <div class="sidebar-caption">
                Analytics workspace
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Your workspace")

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg,#FFFFFF,#E8F7F0);
            border: 1px solid #D9EAE1;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 10px;
        ">
            <div style="font-size:1.45rem;">✦</div>
            <div style="font-weight:750;color:#302746;">
                Bring your request logs
            </div>
            <div style="
                font-size:0.8rem;
                color:#786F89;
                line-height:1.5;
                margin-top:5px;
            ">
                Explore model costs, response times and caching
                performance from one place.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload your request logs",
        type=["csv"],
        help=(
            "Required: model, complexity, latency and cost. "
            "Cache status and timestamp are recommended."
        ),
    )

    if uploaded_file is not None:
        try:
            raw_data = pd.read_csv(uploaded_file)
            df = normalize_dataset(raw_data)
            data_source = uploaded_file.name

            st.success("CSV uploaded and validated.")

        except Exception as exc:
            st.error(f"Could not read your CSV: {exc}")
            st.stop()

    else:
        df = generate_sample_data()
        data_source = "Sample request logs"

        st.info(
            "Using sample data. Upload your own CSV to explore "
            "your request logs."
        )

    st.caption(f"Data source: {data_source}")
    st.caption(f"{len(df):,} valid records loaded")

    st.divider()

    st.markdown("### Explore your data")
    st.caption("Use these filters to update the whole dashboard.")

    all_models = sorted(df["model"].unique().tolist())
    all_complexities = sorted(
        df["complexity"].unique().tolist()
    )

    selected_models = st.multiselect(
        "Models",
        options=all_models,
        default=all_models,
        help="Choose which models to include.",
    )

    selected_complexities = st.multiselect(
        "Request complexity",
        options=all_complexities,
        default=all_complexities,
    )

    cache_filter = st.selectbox(
        "Cache status",
        [
            "All requests",
            "Cache hits only",
            "Cache misses only",
        ],
    )

    search_text = st.text_input(
        "Search request text",
        placeholder="Try: sales, report, Python...",
    )

    if st.button(
        "Reset filters",
        use_container_width=True,
    ):
        st.session_state["reset_filters"] = True
        st.rerun()

    if st.session_state.pop("reset_filters", False):
        st.rerun()


# ============================================================
# 7. APPLY FILTERS
# ============================================================

filtered = df.copy()

if selected_models:
    filtered = filtered[
        filtered["model"].isin(selected_models)
    ]
else:
    filtered = filtered.iloc[0:0]

if selected_complexities:
    filtered = filtered[
        filtered["complexity"].isin(selected_complexities)
    ]
else:
    filtered = filtered.iloc[0:0]

if cache_filter == "Cache hits only":
    filtered = filtered[filtered["cache_hit"]]

elif cache_filter == "Cache misses only":
    filtered = filtered[~filtered["cache_hit"]]

if search_text.strip():
    filtered = filtered[
        filtered["query"]
        .astype(str)
        .str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

if filtered.empty:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">SmartRouter Analytics</div>
            <div class="hero-title">No matching requests</div>
            <div class="hero-subtitle">
                Try selecting more models or complexities,
                changing the cache filter, or clearing your search.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# 8. CALCULATE KEY METRICS
# ============================================================

total_requests = len(filtered)
total_cost = filtered["estimated_cost"].sum()
average_cost = filtered["estimated_cost"].mean()
average_latency = filtered["latency_ms"].mean()
p95_latency = filtered["latency_ms"].quantile(0.95)
cache_hit_rate = filtered["cache_hit"].mean() * 100

cache_savings = filtered.loc[
    filtered["cache_hit"], "estimated_cost"
].sum()

# Cache savings are zero for this simple sample cost model
# because cache-hit requests have zero estimated cost.
# Real savings require a baseline cost for uncached requests.


# ============================================================
# 9. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">DATA INTELLIGENCE / 01</div>
        <div class="hero-title">SmartRouter Analytics</div>
        <div class="hero-subtitle">
            A clearer view of AI request performance, estimated
            costs, model usage and caching patterns.
            Explore your data and discover where routing can improve.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-label">YOUR DASHBOARD</div>',
    unsafe_allow_html=True,
)

overview_tab, performance_tab, explorer_tab, insights_tab, live_tab, live_analytics_tab, portfolio_tab = (
    st.tabs(
        [
            "Overview",
            "Performance",
            "Request explorer",
            "Insights & data",
            "Live SmartRouter",
            "Live request analytics",
            "Portfolio & guide",
        ]
    )
)


# ============================================================
# 10. OVERVIEW
# ============================================================

with overview_tab:
    st.markdown("### At a glance")
    st.caption(
        f"Showing {total_requests:,} requests after applying filters."
    )

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Total requests",
        f"{total_requests:,}",
    )

    k2.metric(
        "Estimated total cost",
        money(total_cost),
    )

    k3.metric(
        "Average cost / request",
        money(average_cost),
    )

    k4, k5, k6 = st.columns(3)

    k4.metric(
        "Average latency",
        f"{average_latency:,.0f} ms",
    )

    k5.metric(
        "P95 latency",
        f"{p95_latency:,.0f} ms",
        help=(
            "95% of the filtered requests completed at or "
            "below this latency."
        ),
    )

    k6.metric(
        "Cache-hit rate",
        f"{cache_hit_rate:.1f}%",
    )

    st.caption(
        "Sample costs are illustrative estimates, not actual "
        "provider billing. Cache behavior in the sample data "
        "is simulated."
    )

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("### Request activity")

        dated = filtered.dropna(subset=["timestamp"]).copy()

        if not dated.empty:
            dated["date"] = dated["timestamp"].dt.date

            activity = (
                dated.groupby("date")
                .size()
                .reset_index(name="requests")
            )

            fig = px.line(
                activity,
                x="date",
                y="requests",
                markers=True,
                color_discrete_sequence=[SEAFOAM],
                labels={
                    "date": "Date",
                    "requests": "Requests",
                },
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=7),
                hovertemplate=(
                    "Date: %{x}<br>"
                    "Requests: %{y}<extra></extra>"
                ),
            )

            style_chart(fig, 350)
            st.plotly_chart(
                fig,
                use_container_width=True,
            )
        else:
            st.info(
                "No valid timestamps are available for the "
                "activity chart."
            )

    with right:
        st.markdown("### Model distribution")

        model_counts = (
            filtered["model"]
            .value_counts()
            .rename_axis("model")
            .reset_index(name="requests")
        )

        fig = px.pie(
            model_counts,
            names="model",
            values="requests",
            hole=0.68,
            color_discrete_sequence=PALETTE,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "%{label}<br>"
                "Requests: %{value}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )

        style_chart(fig, 350)
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown("### Cost overview")

    cost_by_model = (
        filtered.groupby("model", as_index=False)
        ["estimated_cost"].sum()
        .sort_values("estimated_cost", ascending=False)
    )

    fig = px.bar(
        cost_by_model,
        x="model",
        y="estimated_cost",
        color="model",
        color_discrete_sequence=PALETTE,
        text="estimated_cost",
        labels={
            "model": "Model",
            "estimated_cost": "Estimated cost ($)",
        },
    )

    fig.update_traces(
        texttemplate="$%{y:.5f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(showlegend=False)
    style_chart(fig, 350)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# 11. PERFORMANCE
# ============================================================

with performance_tab:
    st.markdown("### Performance analysis")
    st.caption(
        "Compare response speed, request complexity and cache behavior."
    )

    left, right = st.columns(2)

    with left:
        st.markdown("#### Latency by model")

        fig = px.box(
            filtered,
            x="model",
            y="latency_ms",
            color="model",
            color_discrete_sequence=PALETTE,
            points="outliers",
            labels={
                "model": "Model",
                "latency_ms": "Latency (ms)",
            },
        )

        style_chart(fig, 370)
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:
        st.markdown("#### Cost by complexity")

        complexity_cost = (
            filtered.groupby(
                "complexity", as_index=False
            )["estimated_cost"]
            .mean()
        )

        fig = px.bar(
            complexity_cost,
            x="complexity",
            y="estimated_cost",
            color="complexity",
            color_discrete_sequence=PALETTE,
            labels={
                "complexity": "Complexity",
                "estimated_cost": "Average cost ($)",
            },
        )

        style_chart(fig, 370)
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown("#### Cache performance")

    cache_summary = (
        filtered.assign(
            cache_label=np.where(
                filtered["cache_hit"],
                "Cache hit",
                "Cache miss",
            )
        )
        .groupby("cache_label", as_index=False)
        .agg(
            requests=("request_id", "count"),
            average_latency=("latency_ms", "mean"),
        )
    )

    if not cache_summary.empty:
        left, right = st.columns(2)

        with left:
            fig = px.bar(
                cache_summary,
                x="cache_label",
                y="requests",
                color="cache_label",
                color_discrete_map={
                    "Cache hit": SEAFOAM,
                    "Cache miss": PEACH,
                },
                labels={
                    "cache_label": "Cache status",
                    "requests": "Requests",
                },
            )

            style_chart(fig, 330)
            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with right:
            fig = px.bar(
                cache_summary,
                x="cache_label",
                y="average_latency",
                color="cache_label",
                color_discrete_map={
                    "Cache hit": SEAFOAM,
                    "Cache miss": PEACH,
                },
                labels={
                    "cache_label": "Cache status",
                    "average_latency": "Average latency (ms)",
                },
            )

            style_chart(fig, 330)
            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # --------------------------------------------------------
    # LIVE ROUTER PERFORMANCE EVALUATION (MILESTONE 3)
    # --------------------------------------------------------
    st.divider()
    st.markdown("### Live SmartRouter evaluation")
    st.caption(
        "Performance metrics calculated from requests processed in the "
        "Live SmartRouter tab during this Streamlit session."
    )

    if st.button(
        "Refresh live evaluation",
        key="refresh_live_evaluation",
        help="Reload the evaluation using the latest live request history.",
    ):
        st.rerun()

    live_records = st.session_state.get("live_request_log", [])
    live_eval = pd.DataFrame(live_records)

    if live_eval.empty:
        st.info(
            "No live requests have been recorded yet. Open the Live SmartRouter "
            "tab, submit a few questions, then return here and refresh the evaluation."
        )
    else:
        # Normalize values defensively so older session records remain usable.
        live_eval["latency_ms"] = pd.to_numeric(
            live_eval.get("latency_ms", pd.Series(dtype=float)), errors="coerce"
        )
        live_eval["cache_hit"] = live_eval.get(
            "cache_hit", pd.Series(False, index=live_eval.index)
        ).fillna(False).astype(bool)
        live_eval["complexity"] = live_eval.get(
            "complexity", pd.Series("Unknown", index=live_eval.index)
        ).fillna("Unknown").astype(str)
        live_eval["route"] = live_eval.get(
            "route", pd.Series("Unknown route", index=live_eval.index)
        ).fillna("Unknown route").astype(str)
        live_eval = live_eval.dropna(subset=["latency_ms"])

        if live_eval.empty:
            st.warning("Live request history does not contain valid latency measurements yet.")
        else:
            live_total = len(live_eval)
            live_hits = int(live_eval["cache_hit"].sum())
            live_misses = live_total - live_hits
            live_hit_rate = (live_hits / live_total) * 100
            live_avg_latency = live_eval["latency_ms"].mean()
            live_p95_latency = live_eval["latency_ms"].quantile(0.95)

            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Live requests", f"{live_total:,}")
            e2.metric("Live cache-hit rate", f"{live_hit_rate:.1f}%")
            e3.metric("Average live latency", f"{live_avg_latency:.2f} ms")
            e4.metric("P95 live latency", f"{live_p95_latency:.2f} ms")

            st.caption(
                f"{live_hits:,} cache hits · {live_misses:,} cache misses · "
                "Measurements are local prototype timings, not hosted-model benchmarks."
            )

            eval_left, eval_right = st.columns(2)
            with eval_left:
                st.markdown("#### Request complexity distribution")
                complexity_counts = (
                    live_eval["complexity"].value_counts()
                    .rename_axis("complexity")
                    .reset_index(name="requests")
                )
                complexity_fig = px.pie(
                    complexity_counts,
                    names="complexity",
                    values="requests",
                    hole=0.62,
                    color_discrete_sequence=PALETTE,
                )
                complexity_fig.update_traces(
                    textinfo="label+percent",
                    hovertemplate="%{label}<br>Requests: %{value}<extra></extra>",
                )
                style_chart(complexity_fig, 330)
                st.plotly_chart(complexity_fig, use_container_width=True)

            with eval_right:
                st.markdown("#### Route usage")
                route_counts = (
                    live_eval["route"].value_counts()
                    .rename_axis("route")
                    .reset_index(name="requests")
                )
                route_fig = px.bar(
                    route_counts,
                    x="requests",
                    y="route",
                    orientation="h",
                    color="route",
                    color_discrete_sequence=PALETTE,
                    labels={"route": "Selected route", "requests": "Requests"},
                )
                route_fig.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
                style_chart(route_fig, 330)
                st.plotly_chart(route_fig, use_container_width=True)

            st.markdown("#### Latency by cache status")
            latency_summary = (
                live_eval.assign(
                    cache_status=np.where(live_eval["cache_hit"], "Cache hit", "Cache miss")
                )
                .groupby("cache_status", as_index=False)
                .agg(
                    requests=("latency_ms", "count"),
                    average_latency_ms=("latency_ms", "mean"),
                    median_latency_ms=("latency_ms", "median"),
                    p95_latency_ms=("latency_ms", lambda values: values.quantile(0.95)),
                )
            )
            latency_cols = st.columns(2)
            with latency_cols[0]:
                latency_fig = px.bar(
                    latency_summary,
                    x="cache_status",
                    y="average_latency_ms",
                    color="cache_status",
                    color_discrete_map={"Cache hit": SEAFOAM, "Cache miss": PEACH},
                    labels={
                        "cache_status": "Cache status",
                        "average_latency_ms": "Average latency (ms)",
                    },
                )
                style_chart(latency_fig, 320)
                st.plotly_chart(latency_fig, use_container_width=True)
            with latency_cols[1]:
                st.dataframe(
                    latency_summary.round(3),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "cache_status": "Cache status",
                        "requests": st.column_config.NumberColumn("Requests", format="%d"),
                        "average_latency_ms": st.column_config.NumberColumn("Average (ms)", format="%.3f"),
                        "median_latency_ms": st.column_config.NumberColumn("Median (ms)", format="%.3f"),
                        "p95_latency_ms": st.column_config.NumberColumn("P95 (ms)", format="%.3f"),
                    },
                )

            st.markdown("#### Complexity and route breakdown")
            breakdown = (
                live_eval.groupby(["complexity", "route"], as_index=False)
                .agg(
                    requests=("latency_ms", "count"),
                    average_latency_ms=("latency_ms", "mean"),
                    cache_hits=("cache_hit", "sum"),
                )
            )
            st.dataframe(
                breakdown.round(3),
                use_container_width=True,
                hide_index=True,
            )

            export_columns = [
                column for column in [
                    "query", "complexity", "complexity_score", "route",
                    "route_profile", "cache_hit", "similarity", "latency_ms", "model",
                ] if column in live_eval.columns
            ]
            st.download_button(
                "Download live performance evaluation (CSV)",
                data=live_eval[export_columns].to_csv(index=False).encode("utf-8-sig"),
                file_name="smartrouter_live_performance_evaluation.csv",
                mime="text/csv",
            )

            st.info(
                "Interpretation note: this evaluation reports observed timings and "
                "routing counts from the local prototype. It does not claim real "
                "LLM provider cost savings or a controlled speed-up comparison."
            )


            # --------------------------------------------------------
            # COST OPTIMIZATION SIMULATOR (MILESTONE 4)
            # --------------------------------------------------------
            st.divider()
            st.markdown("### Cost optimization simulator")
            st.caption(
                "Scenario-based estimate using editable illustrative model rates. "
                "These are not actual charges: the current SmartRouter responder is local and does not call paid LLM APIs."
            )

            with st.expander("Configure illustrative model pricing", expanded=True):
                st.write(
                    "Enter hypothetical USD prices per 1 million tokens. "
                    "Use a provider's published rates if you later connect a real model."
                )
                price_cols = st.columns(3)
                fast_input_rate = price_cols[0].number_input(
                    "Fast route input ($ / 1M tokens)", min_value=0.0,
                    value=0.15, step=0.05, format="%.4f", key="m4_fast_in"
                )
                fast_output_rate = price_cols[0].number_input(
                    "Fast route output ($ / 1M tokens)", min_value=0.0,
                    value=0.60, step=0.05, format="%.4f", key="m4_fast_out"
                )
                balanced_input_rate = price_cols[1].number_input(
                    "Balanced route input ($ / 1M tokens)", min_value=0.0,
                    value=0.40, step=0.05, format="%.4f", key="m4_bal_in"
                )
                balanced_output_rate = price_cols[1].number_input(
                    "Balanced route output ($ / 1M tokens)", min_value=0.0,
                    value=1.60, step=0.05, format="%.4f", key="m4_bal_out"
                )
                premium_input_rate = price_cols[2].number_input(
                    "Premium route input ($ / 1M tokens)", min_value=0.0,
                    value=1.25, step=0.05, format="%.4f", key="m4_premium_in"
                )
                premium_output_rate = price_cols[2].number_input(
                    "Premium route output ($ / 1M tokens)", min_value=0.0,
                    value=5.00, step=0.05, format="%.4f", key="m4_premium_out"
                )
                baseline_input_rate = st.number_input(
                    "Single-model baseline input ($ / 1M tokens)",
                    min_value=0.0, value=1.25, step=0.05,
                    format="%.4f", key="m4_baseline_in"
                )
                baseline_output_rate = st.number_input(
                    "Single-model baseline output ($ / 1M tokens)",
                    min_value=0.0, value=5.00, step=0.05,
                    format="%.4f", key="m4_baseline_out"
                )

            def _estimate_tokens(value):
                # Rough planning estimate only: approximately four characters/token.
                return max(1, int(np.ceil(len(str(value or "")) / 4)))

            cost_rows = []
            for _, record in live_eval.iterrows():
                query_text = record.get("query", "")
                answer_text = record.get("answer", "")
                input_tokens = _estimate_tokens(query_text)
                output_tokens = _estimate_tokens(answer_text)
                complexity_label = str(record.get("complexity", "Medium"))
                cache_hit_flag = bool(record.get("cache_hit", False))

                if complexity_label == "Simple":
                    route_in, route_out = fast_input_rate, fast_output_rate
                    route_tier = "Fast"
                elif complexity_label == "Complex":
                    route_in, route_out = premium_input_rate, premium_output_rate
                    route_tier = "Premium"
                else:
                    route_in, route_out = balanced_input_rate, balanced_output_rate
                    route_tier = "Balanced"

                baseline_cost = (
                    input_tokens * baseline_input_rate
                    + output_tokens * baseline_output_rate
                ) / 1_000_000
                routed_cost = (
                    0.0 if cache_hit_flag else
                    (input_tokens * route_in + output_tokens * route_out) / 1_000_000
                )
                cost_rows.append({
                    "query": query_text,
                    "complexity": complexity_label,
                    "route": record.get("route", "Unknown"),
                    "cache_hit": cache_hit_flag,
                    "estimated_input_tokens": input_tokens,
                    "estimated_output_tokens": output_tokens,
                    "route_tier": "Cache" if cache_hit_flag else route_tier,
                    "single_model_baseline_usd": baseline_cost,
                    "optimized_scenario_usd": routed_cost,
                    "estimated_savings_usd": baseline_cost - routed_cost,
                })

            cost_eval = pd.DataFrame(cost_rows)
            if not cost_eval.empty:
                baseline_total = float(cost_eval["single_model_baseline_usd"].sum())
                optimized_total = float(cost_eval["optimized_scenario_usd"].sum())
                savings_total = baseline_total - optimized_total
                savings_pct = (savings_total / baseline_total * 100) if baseline_total > 0 else 0.0
                cache_avoided = float(
                    cost_eval.loc[cost_eval["cache_hit"], "single_model_baseline_usd"].sum()
                )

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Single-model baseline", f"${baseline_total:.6f}")
                c2.metric("Optimized scenario", f"${optimized_total:.6f}")
                c3.metric("Estimated savings", f"${savings_total:.6f}")
                c4.metric("Estimated savings rate", f"{savings_pct:.1f}%")

                st.caption(
                    f"Estimated model spend avoided by cache hits: ${cache_avoided:.6f}. "
                    "Cache infrastructure, storage, network and operational costs are excluded."
                )

                chart_left, chart_right = st.columns(2)
                with chart_left:
                    st.markdown("#### Baseline vs optimized scenario")
                    comparison = pd.DataFrame({
                        "Scenario": ["Single-model baseline", "Routing + cache scenario"],
                        "Estimated cost (USD)": [baseline_total, optimized_total],
                    })
                    cost_fig = px.bar(
                        comparison, x="Scenario", y="Estimated cost (USD)",
                        color="Scenario", color_discrete_sequence=[LAVENDER, SEAFOAM],
                        text_auto=".6f",
                    )
                    cost_fig.update_layout(showlegend=False)
                    style_chart(cost_fig, 330)
                    st.plotly_chart(cost_fig, use_container_width=True)

                with chart_right:
                    st.markdown("#### Estimated savings by request")
                    savings_chart = cost_eval.copy()
                    savings_chart["request_number"] = np.arange(1, len(savings_chart) + 1)
                    savings_fig = px.bar(
                        savings_chart, x="request_number", y="estimated_savings_usd",
                        color="route_tier", color_discrete_sequence=PALETTE,
                        labels={
                            "request_number": "Request number",
                            "estimated_savings_usd": "Estimated savings (USD)",
                            "route_tier": "Scenario tier",
                        },
                    )
                    style_chart(savings_fig, 330)
                    st.plotly_chart(savings_fig, use_container_width=True)

                st.markdown("#### Request-level cost estimate")
                display_cost = cost_eval.drop(columns=["query"]).copy()
                st.dataframe(
                    display_cost.round(8), use_container_width=True, hide_index=True,
                    column_config={
                        "single_model_baseline_usd": st.column_config.NumberColumn("Baseline ($)", format="$%.8f"),
                        "optimized_scenario_usd": st.column_config.NumberColumn("Optimized ($)", format="$%.8f"),
                        "estimated_savings_usd": st.column_config.NumberColumn("Savings ($)", format="$%.8f"),
                    },
                )
                st.download_button(
                    "Download cost optimization report (CSV)",
                    data=cost_eval.to_csv(index=False).encode("utf-8-sig"),
                    file_name="smartrouter_cost_optimization_estimate.csv",
                    mime="text/csv",
                )

                st.markdown("#### Automatic cost recommendations")
                if live_hits == 0:
                    st.write("- No cache hits were recorded. Test repeated or semantically similar prompts to evaluate cache reuse.")
                else:
                    st.write(f"- {live_hits} of {live_total} requests used the semantic cache. Review cache relevance before increasing cache reuse.")
                if savings_pct > 0:
                    st.write("- Under the selected pricing assumptions, tiered routing and cache reuse reduce the estimated model spend compared with the single-model baseline.")
                elif savings_pct < 0:
                    st.write("- Under the selected pricing assumptions, the optimized scenario is more expensive. Review the route prices or baseline assumptions.")
                else:
                    st.write("- The two scenarios have equal estimated spend under the selected assumptions.")
                st.write("- Token counts are rough character-based estimates. Replace them with provider-reported token usage when integrating a real LLM.")
            else:
                st.info("No cost estimate can be calculated until live requests are recorded.")


            # --------------------------------------------------------
            # ADVANCED ANALYTICS & VISUALIZATIONS (MILESTONE 5)
            # --------------------------------------------------------
            st.divider()
            st.markdown("### Advanced analytics & visualizations")
            st.caption(
                "Explore live prototype requests by complexity, route and cache status. "
                "These are session-level observations, not production benchmarks."
            )

            analytics_df = live_eval.copy().reset_index(drop=True)
            analytics_df["request_number"] = np.arange(1, len(analytics_df) + 1)
            analytics_df["cache_status"] = np.where(
                analytics_df["cache_hit"], "Cache hit", "Cache miss"
            )
            analytics_df["complexity_score"] = pd.to_numeric(
                analytics_df.get("complexity_score", pd.Series(0, index=analytics_df.index)),
                errors="coerce",
            ).fillna(0)
            analytics_df["latency_ms"] = pd.to_numeric(
                analytics_df["latency_ms"], errors="coerce"
            )
            analytics_df = analytics_df.dropna(subset=["latency_ms"])

            filter_a, filter_b, filter_c = st.columns(3)
            with filter_a:
                selected_complexities = st.multiselect(
                    "Filter complexity",
                    options=sorted(analytics_df["complexity"].unique().tolist()),
                    default=sorted(analytics_df["complexity"].unique().tolist()),
                    key="m5_complexity_filter",
                )
            with filter_b:
                selected_routes = st.multiselect(
                    "Filter route",
                    options=sorted(analytics_df["route"].unique().tolist()),
                    default=sorted(analytics_df["route"].unique().tolist()),
                    key="m5_route_filter",
                )
            with filter_c:
                selected_cache_states = st.multiselect(
                    "Filter cache status",
                    options=["Cache hit", "Cache miss"],
                    default=["Cache hit", "Cache miss"],
                    key="m5_cache_filter",
                )

            analytics_filtered = analytics_df[
                analytics_df["complexity"].isin(selected_complexities)
                & analytics_df["route"].isin(selected_routes)
                & analytics_df["cache_status"].isin(selected_cache_states)
            ].copy()

            if analytics_filtered.empty:
                st.info("No requests match these filters. Select at least one value in each filter.")
            else:
                a1, a2, a3, a4 = st.columns(4)
                a1.metric("Filtered requests", f"{len(analytics_filtered):,}")
                a2.metric("Average latency", f"{analytics_filtered['latency_ms'].mean():.2f} ms")
                a3.metric("Median latency", f"{analytics_filtered['latency_ms'].median():.2f} ms")
                a4.metric("Cache-hit rate", f"{analytics_filtered['cache_hit'].mean() * 100:.1f}%")

                row_left, row_right = st.columns(2)
                with row_left:
                    st.markdown("#### Latency by complexity")
                    complexity_latency = (
                        analytics_filtered.groupby("complexity", as_index=False)
                        .agg(requests=("latency_ms", "size"), average_latency_ms=("latency_ms", "mean"))
                    )
                    complexity_order = ["Simple", "Medium", "Complex"]
                    complexity_latency["complexity"] = pd.Categorical(
                        complexity_latency["complexity"], categories=complexity_order, ordered=True
                    )
                    complexity_latency = complexity_latency.sort_values("complexity")
                    fig_complexity = px.bar(
                        complexity_latency, x="complexity", y="average_latency_ms",
                        color="complexity", text_auto=".2f",
                        color_discrete_sequence=PALETTE,
                        labels={"complexity": "Complexity", "average_latency_ms": "Average latency (ms)"},
                    )
                    style_chart(fig_complexity, 330)
                    st.plotly_chart(fig_complexity, use_container_width=True)

                with row_right:
                    st.markdown("#### Cache effectiveness")
                    cache_latency = (
                        analytics_filtered.groupby("cache_status", as_index=False)
                        .agg(requests=("latency_ms", "size"), average_latency_ms=("latency_ms", "mean"))
                    )
                    fig_cache = px.bar(
                        cache_latency, x="cache_status", y="average_latency_ms",
                        color="cache_status", text_auto=".2f",
                        color_discrete_sequence=[SEAFOAM, PEACH],
                        labels={"cache_status": "Cache status", "average_latency_ms": "Average latency (ms)"},
                    )
                    style_chart(fig_cache, 330)
                    st.plotly_chart(fig_cache, use_container_width=True)

                row_left2, row_right2 = st.columns(2)
                with row_left2:
                    st.markdown("#### Request latency trend")
                    trend_fig = px.line(
                        analytics_filtered.sort_values("request_number"),
                        x="request_number", y="latency_ms", color="complexity",
                        markers=True, color_discrete_sequence=PALETTE,
                        labels={"request_number": "Request sequence", "latency_ms": "Latency (ms)"},
                    )
                    style_chart(trend_fig, 330)
                    st.plotly_chart(trend_fig, use_container_width=True)

                with row_right2:
                    st.markdown("#### Complexity score vs latency")
                    scatter_fig = px.scatter(
                        analytics_filtered, x="complexity_score", y="latency_ms",
                        color="complexity", symbol="cache_status", hover_data=["route"],
                        color_discrete_sequence=PALETTE,
                        labels={"complexity_score": "Complexity score", "latency_ms": "Latency (ms)"},
                    )
                    style_chart(scatter_fig, 330)
                    st.plotly_chart(scatter_fig, use_container_width=True)

                st.markdown("#### Route performance summary")
                route_summary = (
                    analytics_filtered.groupby("route", as_index=False)
                    .agg(
                        requests=("latency_ms", "size"),
                        average_latency_ms=("latency_ms", "mean"),
                        median_latency_ms=("latency_ms", "median"),
                        cache_hits=("cache_hit", "sum"),
                    )
                )
                route_summary["cache_hit_rate_pct"] = (
                    route_summary["cache_hits"] / route_summary["requests"] * 100
                )
                st.dataframe(
                    route_summary.round(2), use_container_width=True, hide_index=True,
                    column_config={
                        "average_latency_ms": st.column_config.NumberColumn("Average latency (ms)", format="%.2f"),
                        "median_latency_ms": st.column_config.NumberColumn("Median latency (ms)", format="%.2f"),
                        "cache_hit_rate_pct": st.column_config.NumberColumn("Cache-hit rate", format="%.1f%%"),
                    },
                )

                st.markdown("#### Analytical observations")
                fastest_complexity = complexity_latency.dropna(subset=["average_latency_ms"])
                if not fastest_complexity.empty:
                    fastest_row = fastest_complexity.loc[fastest_complexity["average_latency_ms"].idxmin()]
                    st.write(
                        f"- Lowest observed average latency by complexity: **{fastest_row['complexity']}** "
                        f"({fastest_row['average_latency_ms']:.2f} ms)."
                    )
                if analytics_filtered["cache_hit"].any() and (~analytics_filtered["cache_hit"]).any():
                    hit_avg = analytics_filtered.loc[analytics_filtered["cache_hit"], "latency_ms"].mean()
                    miss_avg = analytics_filtered.loc[~analytics_filtered["cache_hit"], "latency_ms"].mean()
                    st.write(
                        f"- Observed average latency: cache hits **{hit_avg:.2f} ms**, "
                        f"cache misses **{miss_avg:.2f} ms**. Treat this as a small-sample observation; "
                        "repeat tests before drawing a performance conclusion."
                    )
                else:
                    st.write("- Submit both cache-hit and cache-miss requests to compare their observed latency.")
                st.write("- Request sequence is used as the trend axis because the current live log does not store a timestamp for each request.")

                export_cols = [
                    col for col in ["request_number", "query", "complexity", "complexity_score", "route", "cache_status", "latency_ms"]
                    if col in analytics_filtered.columns
                ]
                st.download_button(
                    "Download filtered advanced analytics (CSV)",
                    data=analytics_filtered[export_cols].to_csv(index=False).encode("utf-8-sig"),
                    file_name="smartrouter_advanced_analytics.csv",
                    mime="text/csv",
                    key="m5_advanced_analytics_download",
                )


                # --------------------------------------------------------
                # AI-POWERED INSIGHTS (MILESTONE 6)
                # --------------------------------------------------------
                st.divider()
                st.markdown("### AI-powered performance insights")
                st.caption(
                    "Explainable, automatically generated recommendations based on the "
                    "selected live-session data. This local prototype does not send requests to an LLM."
                )

                insight_lines = []
                insight_lines.append(
                    f"The selected dataset contains {len(analytics_filtered)} requests, "
                    f"with average latency of {analytics_filtered['latency_ms'].mean():.2f} ms "
                    f"and median latency of {analytics_filtered['latency_ms'].median():.2f} ms."
                )

                cache_rate = float(analytics_filtered["cache_hit"].mean() * 100)
                hit_count = int(analytics_filtered["cache_hit"].sum())
                miss_count = int((~analytics_filtered["cache_hit"].astype(bool)).sum())
                if cache_rate == 0:
                    insight_lines.append(
                        "Cache opportunity: no cache hits appear in the current filtered sample. "
                        "Try repeating identical or semantically similar prompts, then review cache reuse."
                    )
                elif cache_rate < 30:
                    insight_lines.append(
                        f"Cache opportunity: the cache-hit rate is {cache_rate:.1f}% ({hit_count} hits out of "
                        f"{len(analytics_filtered)} requests). Test more repeated prompts and review the similarity threshold."
                    )
                else:
                    insight_lines.append(
                        f"Cache usage: {cache_rate:.1f}% of the selected requests were cache hits. "
                        "Continue checking answer relevance when tuning cache reuse."
                    )

                if not route_summary.empty:
                    fastest_route = route_summary.loc[route_summary["average_latency_ms"].idxmin()]
                    slowest_route = route_summary.loc[route_summary["average_latency_ms"].idxmax()]
                    insight_lines.append(
                        f"Route observation: {fastest_route['route']} has the lowest observed average latency "
                        f"({fastest_route['average_latency_ms']:.2f} ms); {slowest_route['route']} has the highest "
                        f"({slowest_route['average_latency_ms']:.2f} ms). Route comparisons are descriptive, "
                        "because request complexity and cache status may differ."
                    )

                if analytics_filtered["latency_ms"].nunique() > 1:
                    q1 = analytics_filtered["latency_ms"].quantile(0.25)
                    q3 = analytics_filtered["latency_ms"].quantile(0.75)
                    iqr = q3 - q1
                    upper_fence = q3 + 1.5 * iqr
                    unusual = analytics_filtered[analytics_filtered["latency_ms"] > upper_fence]
                    if not unusual.empty:
                        insight_lines.append(
                            f"Latency review: {len(unusual)} request(s) are above the IQR-based upper fence "
                            f"({upper_fence:.2f} ms). Inspect those requests before treating them as true outliers."
                        )
                    else:
                        insight_lines.append(
                            "Latency stability: no observations exceed the IQR-based upper fence in this filtered sample."
                        )
                else:
                    insight_lines.append(
                        "Latency review: more requests with varied response times are needed to assess unusual latency."
                    )

                complexity_counts = analytics_filtered["complexity"].value_counts()
                if len(complexity_counts):
                    dominant_complexity = complexity_counts.index[0]
                    insight_lines.append(
                        f"Workload mix: {dominant_complexity} requests are the largest group "
                        f"({int(complexity_counts.iloc[0])} of {len(analytics_filtered)} selected requests)."
                    )

                with st.container(border=True):
                    st.markdown("#### Performance summary")
                    st.write(insight_lines[0])
                    insight_cols = st.columns(3)
                    insight_cols[0].metric("Cache hits", f"{hit_count}")
                    insight_cols[1].metric("Cache misses", f"{miss_count}")
                    insight_cols[2].metric("Cache-hit rate", f"{cache_rate:.1f}%")
                    st.markdown("#### Recommendations and observations")
                    for item in insight_lines[1:]:
                        st.markdown(f"- {item}")

                insights_text = "SMARTROUTER AUTOMATED PERFORMANCE INSIGHTS\n\n" + "\n".join(
                    f"{index + 1}. {line}" for index, line in enumerate(insight_lines)
                ) + "\n\nNote: Insights are generated from local session measurements. They are not LLM-generated and are not production benchmarks."
                st.download_button(
                    "Download performance insights (TXT)",
                    data=insights_text.encode("utf-8"),
                    file_name="smartrouter_performance_insights.txt",
                    mime="text/plain",
                    key="m6_insights_download",
                )


# ============================================================
# 12. REQUEST EXPLORER
# ============================================================

with explorer_tab:
    st.markdown("### Request explorer")
    st.caption(
        "Search, inspect and download the requests that match your filters."
    )

    explorer_search = st.text_input(
        "Find a request",
        placeholder="Search request ID, query, model or complexity...",
        key="explorer_search",
    )

    request_view = filtered.copy()

    if explorer_search.strip():
        term = explorer_search.strip()

        searchable = (
            request_view["request_id"].astype(str)
            + " "
            + request_view["query"].astype(str)
            + " "
            + request_view["model"].astype(str)
            + " "
            + request_view["complexity"].astype(str)
        )

        request_view = request_view[
            searchable.str.contains(
                term,
                case=False,
                regex=False,
                na=False,
            )
        ]

    display_columns = [
        "request_id",
        "timestamp",
        "query",
        "model",
        "complexity",
        "cache_hit",
        "latency_ms",
        "estimated_cost",
    ]

    st.caption(
        f"{len(request_view):,} matching requests"
    )

    st.dataframe(
        request_view[display_columns],
        use_container_width=True,
        hide_index=True,
        height=420,
        column_config={
            "request_id": st.column_config.TextColumn(
                "Request ID"
            ),
            "timestamp": st.column_config.DatetimeColumn(
                "Timestamp",
                format="YYYY-MM-DD HH:mm",
            ),
            "query": st.column_config.TextColumn(
                "Request text",
                width="large",
            ),
            "model": st.column_config.TextColumn("Model"),
            "complexity": st.column_config.TextColumn(
                "Complexity"
            ),
            "cache_hit": st.column_config.CheckboxColumn(
                "Cache hit"
            ),
            "latency_ms": st.column_config.NumberColumn(
                "Latency",
                format="%.1f ms",
            ),
            "estimated_cost": st.column_config.NumberColumn(
                "Estimated cost",
                format="$%.6f",
            ),
        },
    )

    csv_bytes = request_view.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "Download filtered requests (CSV)",
        data=csv_bytes,
        file_name="smartrouter_filtered_requests.csv",
        mime="text/csv",
        use_container_width=False,
    )

    st.markdown("#### Inspect one request")

    if not request_view.empty:
        request_options = request_view["request_id"].astype(str).tolist()

        chosen_id = st.selectbox(
            "Choose request ID",
            options=request_options,
        )

        selected_request = request_view[
            request_view["request_id"].astype(str) == chosen_id
        ].iloc[0]

        a, b, c = st.columns(3)

        a.metric(
            "Model",
            str(selected_request["model"]),
        )

        b.metric(
            "Latency",
            f"{selected_request['latency_ms']:,.1f} ms",
        )

        c.metric(
            "Estimated cost",
            money(selected_request["estimated_cost"]),
        )

        st.markdown("**Request text**")
        st.write(str(selected_request["query"]))

        st.markdown("**Routing details**")

        st.json(
            {
                "request_id": str(selected_request["request_id"]),
                "model": str(selected_request["model"]),
                "complexity": str(selected_request["complexity"]),
                "cache_hit": bool(selected_request["cache_hit"]),
                "latency_ms": float(selected_request["latency_ms"]),
                "estimated_cost": float(
                    selected_request["estimated_cost"]
                ),
            }
        )
    else:
        st.info("No requests match this search.")


# ============================================================
# 13. INSIGHTS AND DATA QUALITY
# ============================================================

with insights_tab:
    st.markdown("### Insights & data")
    st.caption(
        "Quick observations calculated from the currently filtered data."
    )

    fastest_model = (
        filtered.groupby("model")["latency_ms"]
        .mean()
        .sort_values()
    )

    cheapest_model = (
        filtered.groupby("model")["estimated_cost"]
        .mean()
        .sort_values()
    )

    hit_rate = filtered["cache_hit"].mean() * 100

    insight_cols = st.columns(2)

    with insight_cols[0]:
        if not fastest_model.empty:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-card-title">
                        FASTEST ON AVERAGE
                    </div>
                    <div class="info-card-value">
                        {fastest_model.index[0]}
                    </div>
                    <div class="info-card-description">
                        Average latency:
                        {fastest_model.iloc[0]:,.1f} ms
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with insight_cols[1]:
        if not cheapest_model.empty:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-card-title">
                        LOWEST AVERAGE COST
                    </div>
                    <div class="info-card-value">
                        {cheapest_model.index[0]}
                    </div>
                    <div class="info-card-description">
                        Average estimated cost:
                        ${cheapest_model.iloc[0]:.6f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    insight_cols = st.columns(2)

    with insight_cols[0]:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    CACHE HIT RATE
                </div>
                <div class="info-card-value">
                    {hit_rate:.1f}%
                </div>
                <div class="info-card-description">
                    Share of filtered requests served as cache hits.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_cols[1]:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    P95 RESPONSE LATENCY
                </div>
                <div class="info-card-value">
                    {p95_latency:,.0f} ms
                </div>
                <div class="info-card-description">
                    95% of requests completed within this time.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Automatic observations")

    if not fastest_model.empty:
        st.write(
            f"- **Fastest model:** {fastest_model.index[0]}, "
            f"averaging {fastest_model.iloc[0]:,.1f} ms."
        )

    if not cheapest_model.empty:
        st.write(
            f"- **Lowest average cost:** {cheapest_model.index[0]}, "
            f"at ${cheapest_model.iloc[0]:.6f} per request."
        )

    if hit_rate < 20:
        st.write(
            "- **Caching opportunity:** the cache-hit rate is below 20%. "
            "Review repeated queries and cache eligibility."
        )
    elif hit_rate < 50:
        st.write(
            "- **Caching opportunity:** the cache-hit rate is moderate. "
            "Evaluate whether repeated queries could be cached safely."
        )
    else:
        st.write(
            "- **Caching activity:** more than half of filtered requests "
            "are cache hits. Validate that cached responses remain relevant."
        )

    st.write(
        "- **Cost review:** compare average cost by model and complexity "
        "before choosing routing rules."
    )

    st.write(
        "- **Latency review:** use P95 latency alongside the average to "
        "identify slower requests that an average alone can hide."
    )

    st.divider()

    st.markdown("### Data quality summary")

    quality = pd.DataFrame(
        {
            "Check": [
                "Rows currently analyzed",
                "Missing timestamps",
                "Missing request text",
                "Missing model values",
                "Missing complexity values",
                "Missing latency values",
                "Missing estimated costs",
                "Duplicate request IDs",
            ],
            "Result": [
                f"{len(filtered):,}",
                int(filtered["timestamp"].isna().sum()),
                int(
                    filtered["query"].isna().sum()
                    + (
                        filtered["query"].astype(str).str.strip() == ""
                    ).sum()
                ),
                int(filtered["model"].isna().sum()),
                int(filtered["complexity"].isna().sum()),
                int(filtered["latency_ms"].isna().sum()),
                int(filtered["estimated_cost"].isna().sum()),
                int(filtered["request_id"].duplicated().sum()),
            ],
        }
    )

    st.dataframe(
        quality,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download data quality report",
        data=quality.to_csv(index=False).encode("utf-8-sig"),
        file_name="smartrouter_data_quality.csv",
        mime="text/csv",
    )


# ============================================================
# 14. LIVE SMARTRouter ENGINE
# ============================================================

from smartrouter_engine import SmartRouterEngine

if "smartrouter_engine" not in st.session_state:
    st.session_state.smartrouter_engine = SmartRouterEngine(
        similarity_threshold=0.72
    )

if "live_request_log" not in st.session_state:
    st.session_state.live_request_log = []

if "live_request_counter" not in st.session_state:
    st.session_state.live_request_counter = len(st.session_state.live_request_log)


def record_live_request(result):
    """Add traceable request metadata and retain the latest session records."""
    st.session_state.live_request_counter += 1
    record = result.copy()
    record["request_id"] = f"LIVE-{st.session_state.live_request_counter:04d}"
    record["timestamp"] = datetime.now()
    st.session_state.live_request_log.insert(0, record)
    # Keep a useful session history without allowing it to grow indefinitely.
    st.session_state.live_request_log = st.session_state.live_request_log[:1000]
    st.session_state.latest_live_result = record
    return record


with live_tab:
    st.markdown("### Try the live local router")
    st.caption(
        "Submit questions to test local similarity caching and rule-based routing. "
        "No API key or internet connection is required."
    )

    st.info(
        "Prototype note: this first version uses TF-IDF text similarity and a "
        "local rule-based responder. It is not yet connected to an actual LLM."
    )

    engine = st.session_state.smartrouter_engine

    left_live, right_live = st.columns([1.55, 1])

    with left_live:
        live_query = st.text_area(
            "Enter your question",
            placeholder="Example: Explain machine learning",
            height=115,
            key="live_query_input",
        )

        submit_live = st.button(
            "Process request",
            type="primary",
            use_container_width=True,
            key="process_live_request",
        )

        if submit_live:
            try:
                result = engine.process(live_query)
                record_live_request(result)
            except ValueError as exc:
                st.warning(str(exc))

        st.markdown("#### Try these example questions")
        examples = [
            "What is machine learning?",
            "Explain machine learning",
            "What is semantic caching?",
            "How does a cache work?",
        ]
        example_cols = st.columns(2)
        for index, example in enumerate(examples):
            with example_cols[index % 2]:
                if st.button(
                    example,
                    key=f"live_example_{index}",
                    use_container_width=True,
                ):
                    example_result = engine.process(example)
                    record_live_request(example_result)
                    st.rerun()

        latest = st.session_state.get("latest_live_result")
        if latest:
            st.divider()
            st.markdown("#### Latest response")
            if latest["cache_hit"]:
                st.success("Cache hit — reused a previously stored response.")
            else:
                st.warning("Cache miss — processed and stored a new response.")

            st.write(latest["answer"])

            detail_a, detail_b, detail_c = st.columns(3)
            detail_a.metric("Complexity", latest["complexity"])
            detail_b.metric("Similarity", f'{latest["similarity"]:.1%}')
            detail_c.metric("Latency", f'{latest["latency_ms"]:.2f} ms')

            st.markdown(f"**Selected route:** {latest['route']}")
            st.caption(latest["routing_reason"])

            with st.expander("Request details"):
                st.json(
                    {
                        "query": latest["query"],
                        "complexity": latest["complexity"],
                        "route": latest["route"],
                        "model": latest["model"],
                        "cache_hit": latest["cache_hit"],
                        "similarity_score": round(latest["similarity"], 4),
                        "latency_ms": round(latest["latency_ms"], 3),
                        "stored_cache_entries": latest["cache_size"],
                    }
                )

    with right_live:
        st.markdown("#### Cache controls")
        threshold = st.slider(
            "Similarity threshold",
            min_value=0.40,
            max_value=0.95,
            value=engine.similarity_threshold,
            step=0.01,
            help=(
                "A higher threshold requires questions to be more similar "
                "before a cached answer is reused."
            ),
        )
        engine.similarity_threshold = threshold

        st.metric("Stored cache entries", len(engine.cache))
        st.metric("Requests processed", len(st.session_state.live_request_log))

        if st.button("Clear semantic cache", use_container_width=True):
            engine.clear_cache()
            st.session_state.live_request_log = []
            st.session_state.live_request_counter = 0
            st.session_state.pop("latest_live_result", None)
            st.success("Cache and live request history cleared.")
            st.rerun()

        st.markdown("#### How to test")
        st.markdown(
            "1. Submit **What is machine learning?**\n"
            "2. Submit **Explain machine learning**.\n"
            "3. Compare the cache status and similarity score.\n"
            "4. Try a completely different question."
        )

    if st.session_state.live_request_log:
        st.divider()
        st.markdown("#### Live request history")
        live_history = pd.DataFrame(st.session_state.live_request_log)
        history_columns = [
            "request_id", "timestamp", "query", "route", "route_profile",
            "complexity", "complexity_score", "cache_hit", "similarity",
            "latency_ms",
        ]
        st.dataframe(
            live_history[history_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "request_id": st.column_config.TextColumn("Request ID"),
                "timestamp": st.column_config.DatetimeColumn(
                    "Timestamp", format="YYYY-MM-DD HH:mm:ss"
                ),
                "query": st.column_config.TextColumn("Question", width="large"),
                "route": st.column_config.TextColumn("Route"),
                "route_profile": st.column_config.TextColumn("Route profile"),
                "complexity": st.column_config.TextColumn("Complexity"),
                "complexity_score": st.column_config.NumberColumn("Complexity score"),
                "cache_hit": st.column_config.CheckboxColumn("Cache hit"),
                "similarity": st.column_config.NumberColumn(
                    "Similarity", format="%.1%%"
                ),
                "latency_ms": st.column_config.NumberColumn(
                    "Latency", format="%.2f ms"
                ),
            },
        )
        st.download_button(
            "Download live request history",
            data=live_history.to_csv(index=False).encode("utf-8-sig"),
            file_name="smartrouter_live_history.csv",
            mime="text/csv",
        )




# ============================================================
# 15. LIVE REQUEST ANALYTICS & REPORTING (MILESTONE 7)
# ============================================================

with live_analytics_tab:
    st.markdown("### Live request analytics & reporting")
    st.caption(
        "Search, filter, inspect and export requests submitted through the "
        "Live SmartRouter during this Streamlit session."
    )

    live_records = st.session_state.get("live_request_log", [])
    live_report_df = pd.DataFrame(live_records)

    if live_report_df.empty:
        st.info(
            "No live requests are recorded yet. Open the **Live SmartRouter** "
            "tab, submit a few questions, and return here to explore them."
        )
    else:
        # Backward-compatible defaults for records created before Milestone 7.
        if "request_id" not in live_report_df.columns:
            live_report_df["request_id"] = [
                f"LIVE-OLD-{i:04d}" for i in range(1, len(live_report_df) + 1)
            ]
        if "timestamp" not in live_report_df.columns:
            live_report_df["timestamp"] = pd.NaT

        live_report_df["timestamp"] = pd.to_datetime(
            live_report_df["timestamp"], errors="coerce"
        )
        live_report_df["latency_ms"] = pd.to_numeric(
            live_report_df.get("latency_ms", pd.Series(index=live_report_df.index, dtype=float)),
            errors="coerce",
        )
        live_report_df["cache_hit"] = (
            live_report_df.get("cache_hit", pd.Series(False, index=live_report_df.index))
            .fillna(False)
            .astype(bool)
        )
        for column, default in [
            ("query", ""),
            ("answer", ""),
            ("complexity", "Unknown"),
            ("route", "Unknown route"),
            ("route_profile", "Unknown profile"),
            ("model", "Local responder"),
            ("routing_reason", ""),
        ]:
            if column not in live_report_df.columns:
                live_report_df[column] = default
            live_report_df[column] = live_report_df[column].fillna(default).astype(str)

        # Filters are local to this tab and do not change the other dashboard tabs.
        st.markdown("#### Find and filter requests")
        filter_search, filter_complexity, filter_cache = st.columns([1.5, 1, 1])

        with filter_search:
            live_search = st.text_input(
                "Search request ID or text",
                placeholder="Search a question, answer or ID...",
                key="m7_live_search",
            )
        with filter_complexity:
            complexity_options = sorted(live_report_df["complexity"].unique().tolist())
            live_complexities = st.multiselect(
                "Complexity",
                options=complexity_options,
                default=complexity_options,
                key="m7_live_complexity",
            )
        with filter_cache:
            live_cache_filter = st.selectbox(
                "Cache status",
                ["All requests", "Cache hits only", "Cache misses only"],
                key="m7_live_cache",
            )

        route_options = sorted(live_report_df["route"].unique().tolist())
        selected_live_routes = st.multiselect(
            "Route",
            options=route_options,
            default=route_options,
            key="m7_live_routes",
        )

        live_filtered = live_report_df.copy()
        if live_complexities:
            live_filtered = live_filtered[
                live_filtered["complexity"].isin(live_complexities)
            ]
        else:
            live_filtered = live_filtered.iloc[0:0]

        if selected_live_routes:
            live_filtered = live_filtered[
                live_filtered["route"].isin(selected_live_routes)
            ]
        else:
            live_filtered = live_filtered.iloc[0:0]

        if live_cache_filter == "Cache hits only":
            live_filtered = live_filtered[live_filtered["cache_hit"]]
        elif live_cache_filter == "Cache misses only":
            live_filtered = live_filtered[~live_filtered["cache_hit"]]

        if live_search.strip():
            search_term = live_search.strip()
            searchable = (
                live_filtered["request_id"].astype(str)
                + " " + live_filtered["query"].astype(str)
                + " " + live_filtered["answer"].astype(str)
                + " " + live_filtered["route"].astype(str)
            )
            live_filtered = live_filtered[
                searchable.str.contains(search_term, case=False, regex=False, na=False)
            ]

        # Optional date range, only when usable timestamps exist.
        valid_dates = live_filtered["timestamp"].dropna()
        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            date_col, reset_col = st.columns([2, 5])
            with date_col:
                selected_dates = st.date_input(
                    "Request date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="m7_live_date_range",
                )
            if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
                start_date, end_date = selected_dates
                live_filtered = live_filtered[
                    live_filtered["timestamp"].dt.date.between(start_date, end_date)
                ]

        st.divider()
        st.markdown("#### Session summary")
        live_total_filtered = len(live_filtered)
        live_hits_filtered = int(live_filtered["cache_hit"].sum()) if live_total_filtered else 0
        live_misses_filtered = live_total_filtered - live_hits_filtered
        live_hit_rate_filtered = (
            live_hits_filtered / live_total_filtered * 100 if live_total_filtered else 0
        )
        avg_live_latency_filtered = (
            live_filtered["latency_ms"].mean() if live_total_filtered else 0
        )
        p95_live_latency_filtered = (
            live_filtered["latency_ms"].quantile(0.95) if live_total_filtered else 0
        )

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Matching requests", f"{live_total_filtered:,}")
        m2.metric("Cache hits", f"{live_hits_filtered:,}")
        m3.metric("Cache-hit rate", f"{live_hit_rate_filtered:.1f}%")
        m4.metric("Average latency", f"{avg_live_latency_filtered:.2f} ms")
        m5.metric("P95 latency", f"{p95_live_latency_filtered:.2f} ms")

        st.caption(
            f"{live_misses_filtered:,} cache misses in the current selection. "
            "These are local prototype measurements from this session."
        )

        st.markdown("#### Request history")
        live_table_columns = [
            "request_id", "timestamp", "query", "complexity", "route",
            "cache_hit", "similarity", "latency_ms",
        ]
        available_table_columns = [
            col for col in live_table_columns if col in live_filtered.columns
        ]
        st.caption(f"Showing {len(live_filtered):,} matching live request(s).")
        st.dataframe(
            live_filtered[available_table_columns],
            use_container_width=True,
            hide_index=True,
            height=380,
            column_config={
                "request_id": st.column_config.TextColumn("Request ID"),
                "timestamp": st.column_config.DatetimeColumn(
                    "Timestamp", format="YYYY-MM-DD HH:mm:ss"
                ),
                "query": st.column_config.TextColumn("Question", width="large"),
                "complexity": st.column_config.TextColumn("Complexity"),
                "route": st.column_config.TextColumn("Selected route"),
                "cache_hit": st.column_config.CheckboxColumn("Cache hit"),
                "similarity": st.column_config.NumberColumn("Similarity", format="%.1%%"),
                "latency_ms": st.column_config.NumberColumn("Latency", format="%.2f ms"),
            },
        )

        st.markdown("#### Inspect request details")
        if not live_filtered.empty:
            request_ids = live_filtered["request_id"].astype(str).tolist()
            selected_live_id = st.selectbox(
                "Select a request",
                options=request_ids,
                key="m7_selected_live_request",
            )
            selected_live_record = live_filtered[
                live_filtered["request_id"].astype(str) == selected_live_id
            ].iloc[0]

            detail_a, detail_b, detail_c, detail_d = st.columns(4)
            detail_a.metric("Complexity", selected_live_record["complexity"])
            detail_b.metric("Route", selected_live_record["route"])
            detail_c.metric(
                "Cache status",
                "Hit" if selected_live_record["cache_hit"] else "Miss",
            )
            detail_d.metric(
                "Latency",
                f"{selected_live_record['latency_ms']:.2f} ms"
                if pd.notna(selected_live_record["latency_ms"]) else "N/A",
            )

            with st.expander("View full request and response", expanded=True):
                st.markdown("**Request**")
                st.write(selected_live_record["query"])
                st.markdown("**Local response**")
                st.write(selected_live_record["answer"])
                st.markdown("**Routing explanation**")
                st.write(selected_live_record["routing_reason"] or "No explanation stored.")
                st.markdown("**Additional request metadata**")
                metadata = {
                    "request_id": selected_live_record["request_id"],
                    "timestamp": (
                        selected_live_record["timestamp"].isoformat()
                        if pd.notna(selected_live_record["timestamp"]) else None
                    ),
                    "route_profile": selected_live_record.get("route_profile", "N/A"),
                    "model": selected_live_record.get("model", "N/A"),
                    "complexity_score": selected_live_record.get("complexity_score", None),
                    "similarity": selected_live_record.get("similarity", None),
                    "classification_signals": selected_live_record.get(
                        "classification_signals", []
                    ),
                }
                st.json(metadata)
        else:
            st.info("No requests match the selected filters.")

        st.divider()
        st.markdown("#### Download reports")
        export_df = live_filtered.copy()
        csv_data = export_df.to_csv(index=False).encode("utf-8-sig")

        report_lines = [
            "SMARTROUTER LIVE REQUEST REPORT",
            "=" * 34,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Requests in report: {len(live_filtered)}",
            f"Cache hits: {live_hits_filtered}",
            f"Cache misses: {live_misses_filtered}",
            f"Cache-hit rate: {live_hit_rate_filtered:.2f}%",
            f"Average latency: {avg_live_latency_filtered:.3f} ms",
            f"P95 latency: {p95_live_latency_filtered:.3f} ms",
            "",
            "IMPORTANT: These are local prototype measurements. The responder is "
            "not connected to a hosted LLM, and this report does not represent "
            "provider billing or production performance.",
        ]
        report_text = "\n".join(report_lines)

        download_csv_col, download_report_col = st.columns(2)
        with download_csv_col:
            st.download_button(
                "Download request-level data (CSV)",
                data=csv_data,
                file_name="smartrouter_live_request_analytics.csv",
                mime="text/csv",
                use_container_width=True,
                key="m7_live_csv_download",
            )
        with download_report_col:
            st.download_button(
                "Download session summary (TXT)",
                data=report_text.encode("utf-8"),
                file_name="smartrouter_live_session_report.txt",
                mime="text/plain",
                use_container_width=True,
                key="m7_live_report_download",
            )

        st.caption(
            "The live request history is held in Streamlit session state and is "
            "cleared when you clear the cache/history or when the session ends. "
            "The latest 1,000 requests are retained in the current session."
        )



# ============================================================
# 16. FINAL PORTFOLIO DASHBOARD & PROJECT GUIDE (MILESTONE 8)
# ============================================================

with portfolio_tab:
    st.markdown("### Project portfolio")
    st.caption("Project overview, technical methodology and demo guide.")

    st.markdown(
        '''
        <div class="hero" style="margin-top:12px;">
          <div class="eyebrow">PORTFOLIO PROJECT / FINAL BUILD</div>
          <div class="hero-title">LLM SmartRouter Analytics</div>
          <div class="hero-subtitle">
            An interactive analytics prototype demonstrating how request
            complexity, similarity-based caching and routing decisions can
            be explored through performance metrics.
          </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Core capabilities", "6+")
    p2.metric("Analytics views", "6")
    p3.metric("Live history limit", "1,000")
    p4.metric("External API required", "No")

    st.divider()
    st.markdown("### What this project demonstrates")
    feature_data = [
        ("Semantic-style caching", "TF-IDF vectors and cosine similarity compare incoming questions with cached questions. A configurable threshold determines whether a cached response can be reused."),
        ("Intelligent routing", "A transparent rule-based complexity classifier assigns Simple, Medium or Complex requests to local fast, balanced or deep-analysis routes."),
        ("Performance analytics", "Explore request volume, latency, P95 latency, estimated cost, cache-hit rate and model/request distributions."),
        ("Data exploration", "Upload compatible request-log CSV files, filter records, inspect data quality and explore request-level patterns."),
        ("Explainable insights", "Rule-based insights highlight observed patterns without external Gemini or paid API calls."),
        ("Live request reporting", "Submit local test queries, inspect request IDs and timestamps, filter session history and export CSV/TXT reports."),
    ]
    feature_cols = st.columns(2)
    for index, (feature_title, feature_description) in enumerate(feature_data):
        with feature_cols[index % 2]:
            with st.container(border=True):
                st.markdown(f"**{feature_title}**")
                st.write(feature_description)

    st.divider()
    st.markdown("### How the system works")
    st.markdown(
        '''
        <div style="background:#FFFFFF;border:1px solid #E9E3F0;border-radius:16px;padding:18px;color:#302746;">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:9px;">
            <div style="background:#F0E9FC;border-radius:12px;padding:12px;text-align:center;"><b>Incoming query</b><br><small>Question text</small></div>
            <div style="color:#8B76C5;">→</div>
            <div style="background:#E5F6F0;border-radius:12px;padding:12px;text-align:center;"><b>Cache check</b><br><small>TF-IDF + cosine</small></div>
            <div style="color:#8B76C5;">→</div>
            <div style="background:#FFF0E7;border-radius:12px;padding:12px;text-align:center;"><b>Complexity</b><br><small>Rule-based score</small></div>
            <div style="color:#8B76C5;">→</div>
            <div style="background:#EAF1FC;border-radius:12px;padding:12px;text-align:center;"><b>Local route</b><br><small>Fast / Balanced / Deep</small></div>
          </div>
          <p style="text-align:center;color:#786F89;margin:12px 0 0;">Response and request metadata are logged for live analytics and reporting.</p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown("### Technical methodology")
    method_left, method_right = st.columns(2)
    with method_left:
        st.markdown("**Caching and routing**")
        st.write(
            "- Text is cleaned and vectorized with TF-IDF.\n"
            "- Cosine similarity measures closeness to cached queries.\n"
            "- Default cache threshold: 0.72.\n"
            "- Rule-based keyword and request-length signals estimate complexity.\n"
            "- Routes are local processing profiles, not hosted models."
        )
    with method_right:
        st.markdown("**Analytics and reporting**")
        st.write(
            "- Pandas handles data preparation, filtering and aggregation.\n"
            "- Plotly provides interactive charts.\n"
            "- Streamlit session state stores live request history.\n"
            "- Average and P95 latency summarize observed local timings.\n"
            "- CSV and TXT downloads support further inspection."
        )

    with st.expander("Metric definitions"):
        st.markdown(
            "| Metric | Meaning |\\n|---|---|\\n"
            "| Cache-hit rate | Percentage of included requests served from cache. |\\n"
            "| Similarity | Cosine similarity between incoming and cached queries. |\\n"
            "| Average latency | Mean measured request latency in milliseconds. |\\n"
            "| P95 latency | 95th percentile of measured request latency. |\\n"
            "| Estimated cost | Illustrative value based on uploaded/sample dataset assumptions. |"
        )

    with st.expander("Important scope and limitations"):
        st.warning(
            "This is a local educational and portfolio prototype. The live responder "
            "is rule-based, the cache uses TF-IDF rather than neural embeddings, and "
            "the routes are local profiles rather than actual hosted LLMs."
        )
        st.write(
            "- Cost values are illustrative estimates, not provider invoices.\n"
            "- Live latency depends on the local machine and is not a production benchmark.\n"
            "- Live request history is session-scoped, not a persistent database.\n"
            "- The complexity classifier uses transparent rules, not a trained ML model."
        )

    st.divider()
    st.markdown("### Suggested project demonstration")
    demo_steps = [
        "Open Overview and explain the dataset source and dashboard filters.",
        "Open Performance and show latency, P95 latency, cache and cost patterns.",
        "Open Request explorer and demonstrate searching and inspecting records.",
        "Open Insights & data and explain observations and data-quality checks.",
        "Open Live SmartRouter; submit a query, then a similar query to demonstrate a possible cache hit.",
        "Open Live request analytics; inspect request IDs, timestamps and export CSV/TXT reports.",
        "Finish here with the architecture, methodology and limitations.",
    ]
    for number, step in enumerate(demo_steps, start=1):
        st.markdown(f"**{number}.** {step}")

    readme_text = "\\n".join([
        "# LLM SmartRouter Analytics",
        "",
        "An interactive Streamlit portfolio prototype for request routing, similarity-based caching, performance analytics and request-level reporting.",
        "",
        "## Features",
        "- TF-IDF + cosine-similarity cache matching",
        "- Rule-based request complexity classification",
        "- Local fast, balanced and deep-analysis route profiles",
        "- Interactive analytics dashboards and CSV exploration",
        "- Explainable insights and live request reporting",
        "",
        "## Tech stack",
        "Python, Streamlit, Pandas, NumPy, Scikit-learn, Plotly",
        "",
        "## Run locally",
        "1. Install dependencies: `pip install streamlit pandas numpy scikit-learn plotly`",
        "2. Keep `app.py` and `smartrouter_engine.py` in the same folder.",
        "3. Run: `streamlit run app.py`",
        "",
        "## Important limitations",
        "This is a local prototype, not a production LLM gateway. The live responder is rule-based and is not connected to hosted LLMs. Route names describe local profiles, not actual model providers. Cost figures are illustrative assumptions, not actual provider billing. Live request history is session-scoped.",
    ])
    st.download_button(
        "Download project README",
        data=readme_text.encode("utf-8"),
        file_name="SmartRouter_README.md",
        mime="text/markdown",
        use_container_width=True,
        key="m8_readme_download",
    )
    st.caption(
        "Present this accurately as a local routing and analytics prototype; "
        "do not claim simulated costs or local route profiles are real hosted-LLM savings."
    )


# ============================================================
# 17. FOOTER
# ============================================================

# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:12px 0;
        color:#817592;
        font-size:0.78rem;
    ">
        SmartRouter Analytics · Pastel Aurora Edition
        <br>
        Built with Python, Streamlit, Pandas and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
