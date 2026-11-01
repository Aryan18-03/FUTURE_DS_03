# ==========================================
# FUTURE INTERNS - TASK 3
# MARKETING FUNNEL & CONVERSION DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------
st.set_page_config(
    page_title="Marketing Funnel Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# DASHBOARD THEME
# ------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #07111f 0%, #0b1728 55%, #101d32 100%);
        color: #edf4ff;
    }
    [data-testid="stSidebar"] {
        background: #0a1423;
        border-right: 1px solid rgba(148, 163, 184, 0.16);
    }
    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.85);
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    .hero {
        padding: 26px 30px;
        border-radius: 18px;
        background: linear-gradient(110deg, rgba(24, 54, 91, .95), rgba(18, 35, 62, .95));
        border: 1px solid rgba(96, 165, 250, .25);
        margin-bottom: 22px;
    }
    .hero-kicker {
        color: #8fc5ff;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .hero h1 {
        color: #f8fbff;
        font-size: 30px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }
    .hero p {
        color: #c3d3e8;
        font-size: 14px;
        margin: 0;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #14243a, #101d30);
        border: 1px solid rgba(120, 160, 210, .22);
        padding: 17px 18px;
        border-radius: 14px;
        min-height: 112px;
    }
    [data-testid="stMetricLabel"] {
        color: #a9bfd9 !important;
        font-size: 13px !important;
    }
    [data-testid="stMetricValue"] {
        color: #f5f9ff !important;
        font-weight: 800 !important;
    }
    .section-heading {
        color: #f0f6ff;
        font-size: 19px;
        font-weight: 700;
        margin: 18px 0 10px 0;
    }
    .section-note {
        color: #9fb2ca;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 12px;
    }
    div[data-testid="stPlotlyChart"] {
        background: #101e31;
        border: 1px solid rgba(120, 160, 210, .18);
        border-radius: 14px;
        padding: 8px;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(120, 160, 210, .18);
        border-radius: 12px;
    }
    .insight {
        background: #11243a;
        border-left: 3px solid #42a5f5;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        color: #d8e6f7;
        font-size: 13px;
    }
    .footer {
        color: #8298b3;
        font-size: 11px;
        text-align: center;
        padding-top: 25px;
    }
    h2, h3 { color: #f0f6ff !important; }
    label, p, span { color: inherit; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# LOAD DATA
# CSV files are stored in the repository root
# ------------------------------------------
@st.cache_data
def load_data():
    leads = pd.read_csv("olist_marketing_qualified_leads_dataset.csv")
    deals = pd.read_csv("olist_closed_deals_dataset.csv")
    return leads, deals

try:
    mql, deals = load_data()
except FileNotFoundError as error:
    st.error("A dataset file could not be found. Please check that both CSV files are uploaded to the main GitHub repository beside app.py.")
    st.code(str(error))
    st.stop()

# ------------------------------------------
# CLEAN DATA
# ------------------------------------------
mql["first_contact_date"] = pd.to_datetime(
    mql["first_contact_date"], errors="coerce"
)
deals["won_date"] = pd.to_datetime(deals["won_date"], errors="coerce")

mql["origin"] = (
    mql["origin"].fillna("Unknown").astype(str).str.strip().str.lower()
)
deals["business_segment"] = deals["business_segment"].fillna("Unknown").astype(str)

# Ensure numeric fields are usable in the scatter plot
deals["declared_product_catalog_size"] = pd.to_numeric(
    deals["declared_product_catalog_size"], errors="coerce"
)
deals["declared_monthly_revenue"] = pd.to_numeric(
    deals["declared_monthly_revenue"], errors="coerce"
)

# ------------------------------------------
# MERGE AND CONVERSION STATUS
# ------------------------------------------
merged = mql.merge(deals, on="mql_id", how="left", indicator=True)
merged["conversion_status"] = np.where(
    merged["_merge"].eq("both"), "Converted", "Not Converted"
)

# ------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.caption("Filter the dashboard by lead source and contact date.")

origin_options = sorted(mql["origin"].dropna().unique().tolist())
selected_origins = st.sidebar.multiselect(
    "Marketing origin",
    options=origin_options,
    default=origin_options,
    format_func=lambda x: "Unknown / Unattributed" if x == "unknown" else x.replace("_", " ").title()
)

valid_dates = mql["first_contact_date"].dropna()
if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()
    selected_dates = st.sidebar.date_input(
        "First contact date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    selected_dates = ()

# Handle both a selected date range and a single selected date
filtered_mql = mql[mql["origin"].isin(selected_origins)].copy()
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_mql = filtered_mql[
        filtered_mql["first_contact_date"].dt.date.between(start_date, end_date)
    ]
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    filtered_mql = filtered_mql[
        filtered_mql["first_contact_date"].dt.date.eq(selected_dates[0])
    ]

filtered_ids = filtered_mql["mql_id"].dropna().unique()
filtered = merged[merged["mql_id"].isin(filtered_ids)].copy()
filtered_deals = deals[deals["mql_id"].isin(filtered_ids)].copy()

# ------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------
total_leads = filtered_mql["mql_id"].nunique()
converted_leads = filtered.loc[
    filtered["conversion_status"] == "Converted", "mql_id"
].nunique()
not_converted = max(total_leads - converted_leads, 0)
conversion_rate = converted_leads / total_leads * 100 if total_leads else 0
drop_off_rate = not_converted / total_leads * 100 if total_leads else 0

# ------------------------------------------
# HEADER
# ------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Future Interns · Data Analytics · Task 03</div>
    <h1>Marketing Funnel & Conversion Performance</h1>
    <p>Understand lead sources, conversion outcomes and the business profile of closed deals.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# KPI CARDS
# ------------------------------------------
st.markdown('<div class="section-heading">Executive Overview</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Marketing Leads", f"{total_leads:,}")
k2.metric("Closed Deals", f"{converted_leads:,}")
k3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
k4.metric("Lead Drop-off", f"{drop_off_rate:.2f}%")

st.markdown(
    '<div class="section-note">Metrics update automatically when you change the filters.</div>',
    unsafe_allow_html=True
)

if total_leads == 0:
    st.warning("No leads match the selected filters. Please select another origin or date range.")
    st.stop()

# ------------------------------------------
# CHART 1: FUNNEL
# ------------------------------------------
st.markdown('<div class="section-heading">1. Lead Conversion Funnel</div>', unsafe_allow_html=True)
st.markdown('<div class="section-note">Shows how many marketing-qualified leads became closed deals.</div>', unsafe_allow_html=True)

funnel_fig = go.Figure(go.Funnel(
    y=["Marketing Qualified Leads", "Closed Deals"],
    x=[total_leads, converted_leads],
    textinfo="value+percent initial",
    marker={"color": ["#3b82f6", "#22c55e"]},
    connector={"line": {"color": "#58708d", "width": 1}}
))
funnel_fig.update_layout(
    template="plotly_dark", height=320, margin=dict(l=20, r=20, t=25, b=20),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#dce9f8"), showlegend=False
)
st.plotly_chart(funnel_fig, use_container_width=True)

# ------------------------------------------
# CHART 2: ORIGIN DISTRIBUTION
# ------------------------------------------
left, right = st.columns(2)
with left:
    st.markdown('<div class="section-heading">2. Leads by Marketing Origin</div>', unsafe_allow_html=True)
    origin_counts = (
        filtered_mql.groupby("origin", as_index=False)["mql_id"].nunique()
        .rename(columns={"mql_id": "leads"})
        .sort_values("leads", ascending=False)
    )
    origin_counts["origin_label"] = origin_counts["origin"].replace(
        {"unknown": "Unknown / Unattributed"}
    ).str.replace("_", " ").str.title()
    donut_fig = px.pie(
        origin_counts, names="origin_label", values="leads", hole=0.62,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    donut_fig.update_traces(
        textposition="inside", textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Leads: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    donut_fig.update_layout(
        template="plotly_dark", height=390, margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.12, font=dict(size=10))
    )
    st.plotly_chart(donut_fig, use_container_width=True)

# ------------------------------------------
# CHART 3: MONTHLY LEAD GENERATION
# ------------------------------------------
with right:
    st.markdown('<div class="section-heading">3. Monthly Lead Generation</div>', unsafe_allow_html=True)
    monthly_leads = (
        filtered_mql.dropna(subset=["first_contact_date"])
        .assign(month=lambda x: x["first_contact_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["mql_id"].nunique()
        .rename(columns={"mql_id": "leads"})
        .sort_values("month")
    )
    if not monthly_leads.empty:
        monthly_fig = px.line(
            monthly_leads, x="month", y="leads", markers=True,
            labels={"month": "Contact Month", "leads": "Marketing Leads"}
        )
        monthly_fig.update_traces(line=dict(color="#60a5fa", width=3), marker=dict(size=7))
        monthly_fig.update_layout(
            template="plotly_dark", height=390, margin=dict(l=15, r=15, t=20, b=35),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,.15)")
        )
        st.plotly_chart(monthly_fig, use_container_width=True)
    else:
        st.info("No valid contact dates are available for this selection.")

# ------------------------------------------
# CHART 4: CLOSED DEALS BY SEGMENT
# ------------------------------------------
left, right = st.columns(2)
with left:
    st.markdown('<div class="section-heading">4. Closed Deals by Business Segment</div>', unsafe_allow_html=True)
    segment_counts = (
        filtered_deals.groupby("business_segment", as_index=False)["mql_id"].nunique()
        .rename(columns={"mql_id": "closed_deals"})
        .sort_values("closed_deals", ascending=False)
    )
    if not segment_counts.empty:
        segment_fig = px.treemap(
            segment_counts, path=["business_segment"], values="closed_deals",
            color="closed_deals", color_continuous_scale="Blues"
        )
        segment_fig.update_traces(
            texttemplate="%{label}<br>%{value:,} deals",
            hovertemplate="<b>%{label}</b><br>Closed deals: %{value:,}<extra></extra>"
        )
        segment_fig.update_layout(
            template="plotly_dark", height=400, margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(segment_fig, use_container_width=True)
    else:
        st.info("No closed deals are available for the selected filters.")

# ------------------------------------------
# CHART 5: CATALOG SIZE VS REVENUE
# ------------------------------------------
with right:
    st.markdown('<div class="section-heading">5. Catalog Size vs Monthly Revenue</div>', unsafe_allow_html=True)
    scatter_data = filtered_deals.dropna(
        subset=["declared_product_catalog_size", "declared_monthly_revenue"]
    ).copy()
    scatter_data = scatter_data[
        (scatter_data["declared_product_catalog_size"] > 0) &
        (scatter_data["declared_monthly_revenue"] > 0)
    ]
    if not scatter_data.empty:
        scatter_fig = px.scatter(
            scatter_data,
            x="declared_product_catalog_size",
            y="declared_monthly_revenue",
            hover_data=["business_segment", "business_type"],
            labels={
                "declared_product_catalog_size": "Product Catalog Size",
                "declared_monthly_revenue": "Declared Monthly Revenue"
            },
            opacity=0.72, color_discrete_sequence=["#38bdf8"]
        )
        scatter_fig.update_yaxes(type="log", title="Monthly Revenue (log scale)")
        scatter_fig.update_layout(
            template="plotly_dark", height=400, margin=dict(l=15, r=15, t=20, b=35),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(148,163,184,.12)"),
            yaxis=dict(gridcolor="rgba(148,163,184,.12)")
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
        st.caption(f"Based on {len(scatter_data):,} closed deals with both values available. Revenue uses a log scale.")
    else:
        st.info("Not enough complete positive catalog and revenue values for this selection.")

# ------------------------------------------
# CHART 6: CONVERSION RATE BY ORIGIN
# ------------------------------------------
st.markdown('<div class="section-heading">6. Conversion Rate by Marketing Origin</div>', unsafe_allow_html=True)
origin_performance = (
    filtered.groupby("origin")
    .agg(
        total_leads=("mql_id", "nunique"),
        converted_leads=("conversion_status", lambda x: filtered.loc[x.index].loc[x.eq("Converted"), "mql_id"].nunique())
    )
    .reset_index()
)
origin_performance["conversion_rate"] = (
    origin_performance["converted_leads"] / origin_performance["total_leads"] * 100
)
origin_performance["origin_label"] = origin_performance["origin"].replace(
    {"unknown": "Unknown / Unattributed"}
).str.replace("_", " ").str.title()
# Unknown is an attribution gap, not a marketing channel; keep it visible but separate.
origin_performance = origin_performance.sort_values("conversion_rate", ascending=True)

conversion_fig = px.bar(
    origin_performance, x="conversion_rate", y="origin_label",
    orientation="h", text=origin_performance["conversion_rate"].map(lambda x: f"{x:.1f}%"),
    labels={"conversion_rate": "Conversion Rate", "origin_label": "Marketing Origin"},
    color="conversion_rate", color_continuous_scale="Blues"
)
conversion_fig.update_traces(
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Conversion rate: %{x:.2f}%<extra></extra>"
)
conversion_fig.update_layout(
    template="plotly_dark", height=max(340, 34 * len(origin_performance)),
    margin=dict(l=10, r=55, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    xaxis=dict(ticksuffix="%", gridcolor="rgba(148,163,184,.15)"),
    yaxis=dict(title="")
)
st.plotly_chart(conversion_fig, use_container_width=True)

# ------------------------------------------
# KEY BUSINESS INSIGHTS
# ------------------------------------------
st.markdown('<div class="section-heading">Key Business Insights</div>', unsafe_allow_html=True)

known_channels = origin_performance[
    origin_performance["origin"] != "unknown"
].copy()

if not known_channels.empty:
    best_rate = known_channels.loc[known_channels["conversion_rate"].idxmax()]
    best_volume = known_channels.loc[known_channels["converted_leads"].idxmax()]
    social_row = known_channels[known_channels["origin"] == "social"]
    email_row = known_channels[known_channels["origin"] == "email"]

    st.markdown(
        f'<div class="insight"><b>Strongest conversion rate:</b> '
        f'{best_rate["origin"].replace("_", " ").title()} leads convert at '
        f'{best_rate["conversion_rate"]:.2f}% among the selected records.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight"><b>Highest closed-deal volume:</b> '
        f'{best_volume["origin"].replace("_", " ").title()} generated '
        f'{int(best_volume["converted_leads"]):,} closed deals.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight"><b>Overall funnel:</b> {conversion_rate:.2f}% of selected '
        f'marketing-qualified leads became closed deals. Review lead qualification and follow-up '
        f'to understand the remaining drop-off.</div>',
        unsafe_allow_html=True
    )

unknown_count = int(filtered_mql.loc[filtered_mql["origin"] == "unknown", "mql_id"].nunique())
if unknown_count:
    st.markdown(
        f'<div class="insight"><b>Attribution opportunity:</b> {unknown_count:,} leads have an '
        f'unknown or missing origin. Improve campaign tagging and source tracking before '
        f'allocating budget based on channel performance.</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------
# DATA DETAILS
# ------------------------------------------
with st.expander("View filtered data and dataset details"):
    st.markdown("**Marketing-qualified leads**")
    st.dataframe(filtered_mql.head(20), use_container_width=True)
    st.markdown("**Closed deals**")
    st.dataframe(filtered_deals.head(20), use_container_width=True)
    st.caption(
        f"Showing up to 20 rows in each preview. Filtered leads: {total_leads:,} · "
        f"Filtered closed deals: {converted_leads:,}."
    )

st.markdown(
    '<div class="footer">Data source: Olist Marketing Funnel public dataset on Kaggle · '
    'Analysis: Future Interns Task 3</div>',
    unsafe_allow_html=True
)
