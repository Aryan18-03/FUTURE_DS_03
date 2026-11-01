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
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
.stApp {
 background:radial-gradient(ellipse at 12% 0%,rgba(20,184,166,.16),transparent 34%),
 radial-gradient(ellipse at 88% 8%,rgba(139,92,246,.19),transparent 32%),
 linear-gradient(145deg,#050914 0%,#0a1020 48%,#0b1426 100%); color:#eef4ff;
}
[data-testid="stHeader"]{background:rgba(5,9,20,.72)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#080f1d,#0d1729);border-right:1px solid rgba(148,163,184,.14)}
[data-testid="stSidebar"] *{color:#d9e6f7}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2{font-size:19px!important;font-weight:800!important;color:#f3f7ff!important}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong{font-size:11px;letter-spacing:1px;color:#5eead4!important}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:12px!important;font-weight:700!important;color:#b8c9df!important}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"]>div,
[data-testid="stSidebar"] [data-testid="stDateInput"] input{background:#111e32!important;border:1px solid rgba(148,163,184,.24)!important;border-radius:9px!important;color:#edf5ff!important;min-height:40px}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.65rem}\n[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2{font-size:19px!important;font-weight:800!important}\n[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:12px;font-weight:700;color:#b8c9df}\n[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.65rem}
.main .block-container{max-width:1500px;padding:2rem 2.5rem 3rem}
.filter-heading{margin:5px 0 12px}
.filter-title{font-size:18px;font-weight:800;color:#f3f7ff;letter-spacing:-.3px}
.filter-subtitle{font-size:12px;color:#91a5c0;margin-top:4px}
[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stSelectbox"]){background:linear-gradient(145deg,rgba(18,31,52,.96),rgba(10,19,34,.98));border:1px solid rgba(94,234,212,.2)!important;border-radius:16px;padding:14px 16px}
[data-testid="stSelectbox"] label,[data-testid="stDateInput"] label{font-size:11px!important;font-weight:700!important;color:#b8c9df!important}
[data-testid="stSelectbox"] [data-baseweb="select"]>div,[data-testid="stDateInput"] input{background:#111e32!important;border:1px solid rgba(148,163,184,.24)!important;border-radius:9px!important;color:#edf5ff!important;min-height:40px}
[data-baseweb="popover"]{background:#111e32!important;border:1px solid rgba(94,234,212,.22)!important}
[data-baseweb="menu"]{background:#111e32!important}
[data-baseweb="menu"] li{color:#e5eefb!important}
[data-baseweb="menu"] li:hover{background:#1b3048!important}
.hero{position:relative;overflow:hidden;padding:36px 40px;border-radius:24px;
 background:linear-gradient(115deg,rgba(13,148,136,.24),rgba(30,64,175,.25) 48%,rgba(109,40,217,.27)),linear-gradient(135deg,#111d33,#10182b);
 border:1px solid rgba(125,211,252,.28);box-shadow:0 18px 55px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.07);margin-bottom:28px}
.hero:after{content:"";position:absolute;width:250px;height:250px;border-radius:50%;right:-70px;top:-130px;background:rgba(45,212,191,.16);filter:blur(8px)}
.hero-kicker{color:#5eead4;font-size:11px;font-weight:800;letter-spacing:2.6px;text-transform:uppercase;margin-bottom:12px}
.hero h1{color:#f8fbff;font-size:clamp(27px,3vw,39px);line-height:1.15;font-weight:800;margin:0 0 11px;letter-spacing:-1.2px}
.hero p{color:#b8c9df;font-size:14px;margin:0;max-width:760px;line-height:1.7}\n.hero-tag{display:inline-block;margin-top:20px;padding:7px 12px;border-radius:999px;background:rgba(45,212,191,.1);border:1px solid rgba(94,234,212,.25);color:#99f6e4;font-size:10px;font-weight:800;letter-spacing:1.2px}
.section-heading{color:#f3f7ff;font-size:19px;font-weight:800;margin:30px 0 12px;letter-spacing:-.3px;padding-left:13px;border-left:3px solid #2dd4bf;text-shadow:0 2px 18px rgba(45,212,191,.12)}
.section-note{color:#91a5c0;font-size:12px;margin-top:-4px;margin-bottom:14px}
.kpi-card{position:relative;overflow:hidden;min-height:132px;padding:19px 20px 17px;border-radius:18px;
 background:linear-gradient(145deg,rgba(23,38,62,.98),rgba(12,22,39,.98));border:1px solid rgba(148,163,184,.2);box-shadow:0 12px 30px rgba(0,0,0,.23)}
.kpi-card:after{content:"";position:absolute;height:3px;left:0;right:0;top:0;background:var(--accent)}
.kpi-top{display:flex;justify-content:space-between;align-items:center;gap:8px;color:#a8bbd3;font-size:11px;font-weight:800;letter-spacing:.5px}
.kpi-icon{display:grid;place-items:center;width:34px;height:34px;border-radius:11px;background:rgba(255,255,255,.07);color:var(--accent);font-size:18px}
.kpi-value{color:#f8fbff;font-size:30px;font-weight:800;letter-spacing:-.8px;margin-top:12px;line-height:1.1}
.kpi-foot{color:#8196b2;font-size:11px;margin-top:7px}
div[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,rgba(18,31,52,.96),rgba(9,17,31,.99));border:1px solid rgba(125,211,252,.16);border-radius:20px;padding:12px 12px 6px;box-shadow:0 16px 36px rgba(0,0,0,.24);transition:border-color .2s ease}\ndiv[data-testid="stPlotlyChart"]:hover{border-color:rgba(45,212,191,.38)}
div[data-testid="stDataFrame"]{border:1px solid rgba(148,163,184,.16);border-radius:14px}
.insight{background:linear-gradient(100deg,rgba(20,184,166,.12),rgba(30,64,175,.12));border:1px solid rgba(94,234,212,.18);border-left:3px solid #2dd4bf;border-radius:12px;padding:14px 17px;margin:10px 0;color:#dce9f8;font-size:13px}
.footer{color:#8196b2;font-size:11px;text-align:center;padding:24px 12px;margin-top:30px;border-top:1px solid rgba(148,163,184,.14)}
h2,h3{color:#f3f7ff!important}
.stCaption,[data-testid="stCaptionContainer"]{color:#91a5c0!important}
hr{border-color:rgba(148,163,184,.14)}
[data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(145deg,rgba(18,31,52,.92),rgba(10,19,34,.96));border:1px solid rgba(94,234,212,.22)!important;border-radius:18px;padding:16px 18px;box-shadow:0 12px 28px rgba(0,0,0,.18)}
[data-testid="stSelectbox"],[data-testid="stMultiSelect"],[data-testid="stDateInput"]{background:rgba(255,255,255,.025);border-radius:10px}
@media(max-width:800px){.main .block-container{padding:1rem}.hero{padding:24px 22px}.kpi-value{font-size:24px}}
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
deals["lead_type"] = deals["lead_type"].fillna("Unknown").astype(str)
deals["business_type"] = deals["business_type"].fillna("Unknown").astype(str)

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
# HEADER
# ------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Future Interns · Data Analytics · Task 03</div>
    <h1>Marketing Funnel & Conversion Performance</h1>
    <p>Explore lead acquisition, conversion outcomes and the business profile of closed deals through an interactive view of the Olist marketing funnel.</p>\n    <div class="hero-tag">INTERACTIVE ANALYTICS · LEAD ACQUISITION · CONVERSION INSIGHTS</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# PROFESSIONAL DASHBOARD FILTERS
# ------------------------------------------
origin_options = sorted(mql["origin"].dropna().unique().tolist())
segment_options = sorted(deals["business_segment"].dropna().unique().tolist())
lead_type_options = sorted(deals["lead_type"].dropna().unique().tolist())
business_type_options = sorted(deals["business_type"].dropna().unique().tolist())

valid_dates = mql["first_contact_date"].dropna()
if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()
else:
    min_date = max_date = pd.Timestamp.today().date()

st.sidebar.markdown("## Dashboard Filters")
st.sidebar.caption("Refine the dashboard using the options below.")
st.sidebar.markdown("---")

st.sidebar.markdown("**LEAD ACQUISITION**")
selected_origin = st.sidebar.selectbox(
    "Marketing origin",
    options=["All"] + origin_options,
    format_func=lambda x: "All origins" if x == "All" else ("Unknown / Unattributed" if x == "unknown" else x.replace("_", " ").title()),
    key="filter_origin"
)
selected_dates = st.sidebar.date_input(
    "First contact period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="filter_contact_date"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**CUSTOMER PROFILE**")
selected_segment = st.sidebar.selectbox(
    "Business segment",
    options=["All"] + segment_options,
    format_func=lambda x: "All segments" if x == "All" else x.replace("_", " ").title(),
    key="filter_segment",
    help="Applies to closed-deal analysis."
)
selected_lead_type = st.sidebar.selectbox(
    "Lead type",
    options=["All"] + lead_type_options,
    format_func=lambda x: "All lead types" if x == "All" else x.replace("_", " ").title(),
    key="filter_lead_type"
)
selected_business_type = st.sidebar.selectbox(
    "Business type",
    options=["All"] + business_type_options,
    format_func=lambda x: "All business types" if x == "All" else x.replace("_", " ").title(),
    key="filter_business_type"
)
st.sidebar.markdown("---")
st.sidebar.caption("All filters update the dashboard automatically.")

# Lead-level filters determine the funnel and overall KPIs.
filtered_mql = mql.copy()
if selected_origin != "All":
    filtered_mql = filtered_mql[filtered_mql["origin"] == selected_origin]

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

# Deal-level filters apply only to charts based on closed-deal attributes.
filtered_deals = deals[deals["mql_id"].isin(filtered_ids)].copy()
if selected_segment != "All":
    filtered_deals = filtered_deals[filtered_deals["business_segment"] == selected_segment]
if selected_lead_type != "All":
    filtered_deals = filtered_deals[filtered_deals["lead_type"] == selected_lead_type]
if selected_business_type != "All":
    filtered_deals = filtered_deals[filtered_deals["business_type"] == selected_business_type]

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
# KPI CARDS
# ------------------------------------------
st.markdown('<div class="section-heading">Executive Overview</div>', unsafe_allow_html=True)
kpi_columns = st.columns(4)
kpi_items = [
    ("TOTAL MARKETING LEADS", f"{total_leads:,}", "♙", "All qualified leads in selection", "#38bdf8"),
    ("CLOSED DEALS", f"{converted_leads:,}", "✦", "Leads that became customers", "#2dd4bf"),
    ("CONVERSION RATE", f"{conversion_rate:.2f}%", "↗", "Share of leads converted", "#a78bfa"),
    ("LEAD DROP-OFF", f"{drop_off_rate:.2f}%", "◌", "Share not yet converted", "#fb7185")
]
for column, (label, value, symbol, foot, accent) in zip(kpi_columns, kpi_items):
    with column:
        st.markdown(
            f'<div class="kpi-card" style="--accent:{accent}">'
            f'<div class="kpi-top"><span>{label}</span><span class="kpi-icon">{symbol}</span></div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-foot">{foot}</div></div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="section-note">Live performance snapshot · Metrics update automatically when sidebar filters change.</div>',
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
