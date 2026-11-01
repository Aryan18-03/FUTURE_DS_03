
# ==========================================
# MARKETING FUNNEL & CONVERSION ANALYSIS
# Future Interns - Task 3
# ==========================================

# Import libraries

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Marketing Funnel Analysis",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# LOAD DATASETS
# ==========================================

@st.cache_data
def load_data():

    mql = pd.read_csv(
        "olist_marketing_qualified_leads_dataset.csv"
    )

    deals = pd.read_csv(
        "olist_closed_deals_dataset.csv"
    )

    return mql, deals


mql, deals = load_data()


# ==========================================
# DATA CLEANING
# ==========================================

# Convert dates into datetime format

mql["first_contact_date"] = pd.to_datetime(
    mql["first_contact_date"],
    errors="coerce"
)

deals["won_date"] = pd.to_datetime(
    deals["won_date"],
    errors="coerce"
)

# Standardize marketing origin

mql["origin"] = (
    mql["origin"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.lower()
)

# Handle missing business segment

deals["business_segment"] = (
    deals["business_segment"]
    .fillna("Unknown")
)


# ==========================================
# MERGE DATASETS
# ==========================================

merged_data = pd.merge(
    mql,
    deals,
    on="mql_id",
    how="left",
    indicator=True
)

# Identify conversion status

merged_data["conversion_status"] = np.where(
    merged_data["_merge"] == "both",
    "Converted",
    "Not Converted"
)


# ==========================================
# CALCULATE KPIs
# ==========================================

total_leads = merged_data["mql_id"].nunique()

converted_leads = (
    merged_data.loc[
        merged_data["conversion_status"] == "Converted",
        "mql_id"
    ].nunique()
)

not_converted = total_leads - converted_leads

conversion_rate = (
    converted_leads / total_leads * 100
    if total_leads else 0
)

drop_off_rate = (
    not_converted / total_leads * 100
    if total_leads else 0
)


# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("📊 Marketing Funnel & Conversion Analysis")

st.markdown(
    "An interactive analysis of marketing-qualified "
    "leads, conversion performance and business outcomes."
)

st.divider()


# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Marketing Leads",
    f"{total_leads:,}"
)

col2.metric(
    "Closed Deals",
    f"{converted_leads:,}"
)

col3.metric(
    "Conversion Rate",
    f"{conversion_rate:.2f}%"
)

col4.metric(
    "Drop-off Rate",
    f"{drop_off_rate:.2f}%"
)

st.divider()


# ==========================================
# DATASET SUMMARY
# ==========================================

st.subheader("Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.write("Marketing Leads Dataset")
    st.dataframe(mql.head(), use_container_width=True)

with col2:
    st.write("Closed Deals Dataset")
    st.dataframe(deals.head(), use_container_width=True)
