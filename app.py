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
:root {
    --bg: #07111F;
    --panel: #0D1B2A;
    --panel-2: #102338;
    --line: #203A53;
    --cyan: #36E4F5;
    --blue: #4D8DFF;
    --violet: #A78BFA;
    --coral: #FF6B81;
    --mint: #4DE2B1;
    --text: #EAF4FF;
    --muted: #91A9C2;
}
.stApp {
    background:
      radial-gradient(ellipse at 12% 0%, rgba(54,228,245,.10), transparent 34%),
      radial-gradient(ellipse at 88% 8%, rgba(167,139,250,.10), transparent 32%),
      var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"], #MainMenu, footer { visibility: hidden !important; }
.block-container { max-width: 1500px; padding: 1.5rem 2rem 2.5rem !important; }
h1, h2, h3 { color: var(--text) !important; letter-spacing: -.025em; }
h1 { font-weight: 800 !important; }
p, label, .stMarkdown { color: var(--text); }
[data-testid="stCaptionContainer"] { color: var(--muted) !important; }
[data-testid="stSidebar"] {
    background: radial-gradient(ellipse at 10% 0%, rgba(54,228,245,.12), transparent 38%),
      linear-gradient(180deg, #0B1B2B 0%, #091522 100%);
    border-right: 1px solid rgba(54,228,245,.22);
}
[data-testid="stSidebar"] * { color: var(--text); }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    color: #FFFFFF !important; font-size: 19px !important; font-weight: 800 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
.sidebar-kicker {
    color: var(--cyan) !important; font-size: .72rem; font-weight: 850; letter-spacing: .16em;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #C8D9EC !important; font-size: .88rem;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    min-height: 42px !important; background: #102338 !important;
    border: 1px solid #36536F !important; border-radius: 9px !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .55rem; }
[data-testid="stSidebar"] hr { border-color: var(--line); margin: .7rem 0; }
[data-testid="stSidebar"] [data-testid="stButton"] button {
    min-height: 44px; background: linear-gradient(100deg, rgba(54,228,245,.18), rgba(167,139,250,.18));
    border: 1px solid rgba(54,228,245,.55); border-radius: 10px;
    color: var(--text); font-weight: 700;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    border-color: var(--cyan); color: var(--cyan);
}
.hero {
    padding: 1.4rem 1.5rem; border: 1px solid rgba(54,228,245,.27);
    border-radius: 18px;
    background: linear-gradient(115deg, rgba(16,35,56,.96), rgba(12,24,42,.83));
    margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(0,0,0,.18);
}
.hero-kicker, .eyebrow {
    color: var(--cyan); font-size: .76rem; font-weight: 800;
    letter-spacing: .16em; text-transform: uppercase; margin-bottom: .55rem;
}
.hero h1 {
    color: #F3F8FF !important; font-size: clamp(1.7rem, 3vw, 2.35rem) !important;
    line-height: 1.2; margin: 0 0 .55rem; letter-spacing: -.04em;
}
.hero p, .hero-sub { color: var(--muted); font-size: .92rem; margin: 0; line-height: 1.6; }
.hero-tag {
    display: inline-block; margin-top: .9rem; padding: .4rem .7rem;
    border-radius: 999px; background: rgba(54,228,245,.09);
    border: 1px solid rgba(54,228,245,.28); color: #A5F3FC;
    font-size: .68rem; font-weight: 800; letter-spacing: .1em;
}
.section-heading {
    padding: .85rem 1.1rem .35rem; margin: 1.35rem 0 .65rem;
    border-left: 3px solid var(--violet);
    background: linear-gradient(100deg, rgba(54,228,245,.07), rgba(167,139,250,.08));
    border-radius: 0 12px 12px 0; color: var(--text);
    font-size: 1.05rem; font-weight: 800; letter-spacing: -.02em;
}
.section-note { color: var(--muted); font-size: .83rem; margin: 0 0 .8rem; }
.kpi-card {
    min-height: 126px; height: 100%; padding: .9rem .95rem;
    border: 1px solid rgba(77,141,255,.30); border-top: 3px solid var(--accent);
    border-radius: 14px; background: linear-gradient(145deg, rgba(13,34,57,.98), rgba(5,19,36,.98));
    box-shadow: 0 8px 24px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.035);
}
.kpi-top { display:flex; align-items:center; justify-content:space-between; gap:.55rem; min-height:30px; }
.kpi-icon {
    display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px;
    border-radius:9px; background:rgba(255,255,255,.07); color:var(--accent); font-size:1.05rem;
}
.kpi-top span:first-child { color:#C8D9EC; font-size:.76rem; font-weight:750; line-height:1.2; }
.kpi-value { color:#F3F8FF; font-size:1.65rem; font-weight:850; letter-spacing:-.04em; margin-top:.45rem; white-space:nowrap; }
.kpi-foot { color:#8FAAC5; font-size:.70rem; margin-top:.12rem; }
div[data-testid="stPlotlyChart"] {
    background: rgba(13,27,42,.74); border: 1px solid var(--line);
    border-radius: 15px; padding: .15rem; overflow: hidden !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.16); margin-bottom: .7rem;
}
[data-testid="stPlotlyChart"] { width:100% !important; min-width:0 !important; overflow:hidden !important; }
[data-testid="stPlotlyChart"] iframe {
    display:block !important; width:100% !important; max-width:100% !important;
    border:0 !important; overflow:hidden !important; scrollbar-width:none !important;
}
[data-testid="stPlotlyChart"] iframe::-webkit-scrollbar,
[data-testid="stPlotlyChart"]::-webkit-scrollbar { display:none !important; width:0 !important; height:0 !important; }
.insight, .insight-card {
    padding: 1rem 1.05rem; border: 1px solid var(--line);
    border-left: 3px solid var(--cyan); background: rgba(13,27,42,.82);
    border-radius: 12px; margin: .65rem 0; color: #DCEBFA; font-size: .88rem; line-height: 1.6;
}
.insight strong, .insight b, .insight-card strong { color: var(--cyan); }
[data-testid="stExpander"] { border:1px solid var(--line); border-radius:12px; background:rgba(13,27,42,.72); }
div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:10px; }
.stButton > button, .stDownloadButton > button {
    border:1px solid rgba(54,228,245,.45);
    background:linear-gradient(100deg, rgba(54,228,245,.14), rgba(77,141,255,.16));
    color:var(--text); border-radius:10px; font-weight:650;
}
.stButton > button:hover, .stDownloadButton > button:hover { border-color:var(--cyan); color:var(--cyan); }
hr { border-color:var(--line); }
.footer { color:var(--muted); font-size:.78rem; text-align:center; padding:1.4rem .7rem; margin-top:1.5rem; border-top:1px solid var(--line); }
@media (max-width: 768px) {
    .block-container { padding:1rem .8rem 2rem !important; }
    .hero { padding:1rem; }
    .kpi-card { min-height:100px; }
    .kpi-value { font-size:1.35rem; }
    div[data-testid="stPlotlyChart"] { padding:0; }
}
</style>
""", unsafe_allow_html=True)

# Hide Plotly's in-chart toolbar so the charts look clean and uncluttered.
CHART_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": False,
    "responsive": True
}

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

def reset_filters():
    """Restore every sidebar filter to its original all-data selection."""
    st.session_state["filter_origin"] = "All"
    st.session_state["filter_contact_date"] = (min_date, max_date)
    st.session_state["filter_segment"] = "All"
    st.session_state["filter_lead_type"] = "All"
    st.session_state["filter_business_type"] = "All"


st.sidebar.markdown("## Dashboard Filters")
st.sidebar.caption("Refine the dashboard using the options below.")
st.sidebar.button(
    "↺  Reset all filters",
    use_container_width=True,
    type="secondary",
    on_click=reset_filters,
    help="Clear every selection and restore the full dataset."
)
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
    ("TOTAL MARKETING LEADS", f"{total_leads:,}", "♙", "All qualified leads in selection", "#36E4F5"),
    ("CLOSED DEALS", f"{converted_leads:,}", "✦", "Leads that became customers", "#4DE2B1"),
    ("CONVERSION RATE", f"{conversion_rate:.2f}%", "↗", "Share of leads converted", "#A78BFA"),
    ("LEAD DROP-OFF", f"{drop_off_rate:.2f}%", "◌", "Share not yet converted", "#FF6B81")
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
# CHART 1: LEAD FUNNEL & OUTCOME
# ------------------------------------------
st.markdown('<div class="section-heading">1. Lead Conversion Funnel & Outcome</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">The first bar shows all marketing-qualified leads. The next two bars split those leads into the two recorded outcomes: closed deals and leads without a matching closed-deal record.</div>',
    unsafe_allow_html=True
)

funnel_data = pd.DataFrame({
    "stage": ["Total Marketing Qualified Leads", "Closed Deals", "Not Converted"],
    "leads": [total_leads, converted_leads, not_converted],
    "share": [
        100.0,
        converted_leads / total_leads * 100 if total_leads else 0,
        not_converted / total_leads * 100 if total_leads else 0
    ],
    "color": ["#4D8DFF", "#4DE2B1", "#FF6B81"]
})

funnel_fig = go.Figure()
for _, row in funnel_data.iterrows():
    funnel_fig.add_trace(go.Bar(
        x=[row["leads"]],
        y=[row["stage"]],
        orientation="h",
        name=row["stage"],
        marker=dict(
            color=row["color"],
            line=dict(color="rgba(255,255,255,0.18)", width=1),
            cornerradius=8
        ),
        text=f'{int(row["leads"]):,}  ·  {row["share"]:.2f}%',
        textposition="outside",
        textfont=dict(color="#EAF4FF", size=13, family="Manrope"),
        cliponaxis=False,
        hovertemplate=(
            f'<b>{row["stage"]}</b><br>'
            'Leads: %{x:,}<br>'
            f'Share of all leads: {row["share"]:.2f}%<extra></extra>'
        ),
        showlegend=False
    ))

funnel_fig.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=105, t=18, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#DCE9F8", family="Manrope"),
    bargap=0.42,
    showlegend=False,
    xaxis=dict(
        title="Number of Leads",
        showgrid=True,
        gridcolor="rgba(148,163,184,.14)",
        zeroline=False,
        range=[0, max(total_leads * 1.18, 1)]
    ),
    yaxis=dict(
        title="",
        autorange="reversed",
        showgrid=False,
        tickfont=dict(size=12, color="#DCE9F8")
    ),
    annotations=[
        dict(
            x=0.99, y=-0.23, xref="paper", yref="paper",
            text="Closed Deals + Not Converted = Total Leads",
            showarrow=False, xanchor="right",
            font=dict(size=10, color="#91A9C2")
        )
    ]
)
st.plotly_chart(funnel_fig, use_container_width=True, config=CHART_CONFIG)

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
    donut_total = int(origin_counts["leads"].sum())
    # Keep labels readable: tiny slices stay in the legend and hover tooltip.
    donut_labels = [
        f"{value / donut_total:.1%}" if donut_total and value / donut_total >= 0.055 else ""
        for value in origin_counts["leads"]
    ]
    donut_fig = px.pie(
        origin_counts, names="origin_label", values="leads", hole=0.66,
        color_discrete_sequence=[
            "#36E4F5", "#4D8DFF", "#A78BFA", "#4DE2B1",
            "#FF6B81", "#60A5FA", "#9B8AFB", "#20B8A5",
            "#F59E0B", "#91A9C2"
        ]
    )
    donut_fig.update_traces(
        text=donut_labels,
        texttemplate="%{text}",
        textposition="inside",
        insidetextorientation="horizontal",
        textfont=dict(size=11, color="#F8FAFC", family="Manrope"),
        marker=dict(line=dict(color="#0B1426", width=3)),
        hovertemplate="<b>%{label}</b><br>Leads: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    donut_fig.update_layout(
        template="plotly_dark",
        height=430,
        margin=dict(l=8, r=8, t=12, b=82),
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="h", y=-0.19, x=0.5, xanchor="center",
            yanchor="top", font=dict(size=9, color="#B8C9DF"),
            bgcolor="rgba(0,0,0,0)", itemwidth=85
        ),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        annotations=[
            dict(
                text=(
                    f"<b style='font-size:27px;color:#FFFFFF'>{donut_total:,}</b>"
                    "<br><span style='font-size:10px;color:#B8C9DF;"
                    "letter-spacing:1.4px'>TOTAL LEADS</span>"
                ),
                x=0.5, y=0.5, xref="paper", yref="paper",
                xanchor="center", yanchor="middle",
                showarrow=False,
                align="center",
                font=dict(size=14, color="#FFFFFF", family="Manrope"),
                bgcolor="rgba(7,17,31,0.92)",
                bordercolor="rgba(54,228,245,0.32)",
                borderwidth=1,
                borderpad=8
            )
        ]
    )
    st.plotly_chart(donut_fig, use_container_width=True, config=CHART_CONFIG)

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
        monthly_fig.update_traces(line=dict(color="#36E4F5", width=3), marker=dict(size=7))
        monthly_fig.update_layout(
            template="plotly_dark", height=390, margin=dict(l=15, r=15, t=20, b=35),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,.15)")
        )
        st.plotly_chart(monthly_fig, use_container_width=True, config=CHART_CONFIG)
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
            color="closed_deals", color_continuous_scale=["#102338", "#36E4F5"]
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
        st.plotly_chart(segment_fig, use_container_width=True, config=CHART_CONFIG)
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
            opacity=0.72, color_discrete_sequence=["#36E4F5"]
        )
        scatter_fig.update_yaxes(type="log", title="Monthly Revenue (log scale)")
        scatter_fig.update_layout(
            template="plotly_dark", height=400, margin=dict(l=15, r=15, t=20, b=35),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(148,163,184,.12)"),
            yaxis=dict(gridcolor="rgba(148,163,184,.12)")
        )
        st.plotly_chart(scatter_fig, use_container_width=True, config=CHART_CONFIG)
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
st.plotly_chart(conversion_fig, use_container_width=True, config=CHART_CONFIG)

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

# ------------------------------------------
# ------------------------------------------
# PROJECT FINDINGS
# ------------------------------------------
st.markdown('<div class="section-heading">Project Findings</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">What the Olist marketing funnel data shows for the current filter selection.</div>',
    unsafe_allow_html=True
)

finding_items = [
    (
        "Lead-to-deal conversion",
        f"{converted_leads:,} of {total_leads:,} marketing-qualified leads are linked to closed deals "
        f"({conversion_rate:.2f}% conversion). {not_converted:,} leads ({drop_off_rate:.2f}%) have no "
        "matching closed-deal record in this dataset."
    )
]

if not known_channels.empty:
    best_rate = known_channels.loc[known_channels["conversion_rate"].idxmax()]
    best_volume = known_channels.loc[known_channels["converted_leads"].idxmax()]
    finding_items.append((
        "Channel quality vs. volume",
        f"{best_rate['origin'].replace('_', ' ').title()} has the highest conversion rate "
        f"({best_rate['conversion_rate']:.2f}%), while "
        f"{best_volume['origin'].replace('_', ' ').title()} produces the most closed deals "
        f"({int(best_volume['converted_leads']):,}). The channel with the best rate is not necessarily "
        "the channel generating the most deals."
    ))

    for channel_name in ["social", "email"]:
        channel_rows = known_channels[known_channels["origin"] == channel_name]
        if not channel_rows.empty:
            channel = channel_rows.iloc[0]
            finding_items.append((
                f"{channel_name.replace('_', ' ').title()} channel result",
                f"{channel_name.replace('_', ' ').title()} records show a "
                f"{channel['conversion_rate']:.2f}% conversion rate "
                f"({int(channel['converted_leads']):,} closed deals from "
                f"{int(channel['total_leads']):,} leads) in the current selection."
            ))

if not segment_counts.empty:
    leading_segment = segment_counts.iloc[0]
    finding_items.append((
        "Business segment mix",
        f"{str(leading_segment['business_segment']).replace('_', ' ').title()} accounts for the "
        f"largest number of closed deals in the selected data "
        f"({int(leading_segment['closed_deals']):,}). This describes the mix of closed deals, "
        "not the segment conversion rate."
    ))

if unknown_count:
    finding_items.append((
        "Lead-source attribution gap",
        f"{unknown_count:,} selected leads have an unknown or missing origin. Their actual marketing "
        "source cannot be identified reliably from the available records."
    ))

for finding_title, finding_text in finding_items:
    st.markdown(
        f'<div class="insight"><b>{finding_title}:</b> {finding_text}</div>',
        unsafe_allow_html=True
    )

# ------------------------------------------
# PROJECT-SPECIFIC RECOMMENDATIONS
# ------------------------------------------
st.markdown('<div class="section-heading">Recommendations</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Actions tied directly to the conversion, channel and segment results above.</div>',
    unsafe_allow_html=True
)

recommendation_items = []

if not known_channels.empty:
    best_rate_name = best_rate["origin"].replace("_", " ").title()
    best_volume_name = best_volume["origin"].replace("_", " ").title()
    recommendation_items.append((
        "Test the strongest converting channel",
        f"Run a controlled budget or lead-generation test for {best_rate_name}, currently the highest "
        f"converting identified channel at {best_rate['conversion_rate']:.2f}%. Increase investment "
        "gradually and compare cost per qualified lead and closed-deal volume before scaling.",
        "Business benefit: validate whether its stronger conversion rate can translate into more deals efficiently."
    ))
    recommendation_items.append((
        "Protect the channel driving deal volume",
        f"Review the campaigns and landing pages behind {best_volume_name}, which contributes the most "
        f"closed deals ({int(best_volume['converted_leads']):,}). Identify which messages and lead sources "
        "are bringing in qualified prospects and retain the effective elements.",
        "Business benefit: maintain the source of the largest current closed-deal contribution."
    ))

for channel_name in ["social", "email"]:
    channel_rows = known_channels[known_channels["origin"] == channel_name] if not known_channels.empty else pd.DataFrame()
    if not channel_rows.empty:
        channel = channel_rows.iloc[0]
        recommendation_items.append((
            f"Review {channel_name.replace('_', ' ')} lead quality",
            f"Audit targeting, campaign message and landing-page relevance for "
            f"{channel_name.replace('_', ' ')}. Its current conversion rate is "
            f"{channel['conversion_rate']:.2f}%; test changes on a small campaign before shifting budget.",
            "Business benefit: identify whether low conversion is caused by targeting, offer or follow-up."
        ))

if unknown_count:
    recommendation_items.append((
        "Fix Olist lead-source attribution",
        "Standardize the origin field and campaign tagging for landing-page and marketing leads. "
        "Investigate why records are stored as unknown or missing, and monitor the unattributed share.",
        "Business benefit: make channel-level conversion comparisons and future marketing allocation more dependable."
    ))

recommendation_items.append((
    "Work on the MQL-to-closed-deal gap",
    f"Review the lead hand-off and follow-up process for the {not_converted:,} selected leads without "
    "a matching closed-deal record. Segment the review by origin and first-contact period, then track "
    "response time and follow-up completion.",
    "Business benefit: identify where qualified leads are being lost between marketing and sales."
))

if not segment_counts.empty:
    segment_name = str(leading_segment["business_segment"]).replace("_", " ").title()
    recommendation_items.append((
        "Study the leading business segment",
        f"Compare the needs, lead sources and sales approach of businesses in {segment_name}, the largest "
        "closed-deal segment in the current selection. Use the segment mix to guide further investigation, "
        "not as proof of a higher conversion rate.",
        "Business benefit: help tailor sales conversations to the customer segments already represented in closed deals."
    ))

for recommendation_title, recommendation_text, benefit_text in recommendation_items:
    st.markdown(
        f'<div class="insight"><b>{recommendation_title}</b><br>{recommendation_text}'
        f'<br><span style="color:#5eead4;font-size:12px;">{benefit_text}</span></div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="footer">Data source: Olist Marketing Funnel public dataset on Kaggle · '
    'Analysis: Future Interns Task 3</div>',
    unsafe_allow_html=True
)
