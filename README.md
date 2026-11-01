# Marketing Funnel & Conversion Performance Analysis

An interactive data analytics dashboard built with **Python and Streamlit** for **Future Interns – Data Science & Analytics Task 3**. The project explores how marketing-qualified leads move through the Olist marketing funnel, which acquisition sources generate closed deals, and what the closed-deal customer profile looks like.

**Live dashboard:** https://futureds03-khuemcchuralwposb29n6u.streamlit.app/  
**GitHub repository:** https://github.com/Aryan18-03/FUTURE_DS_03  
**Dataset source:** [Olist Marketing Funnel – Kaggle](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist)

---

## Project objective

The objective is to analyse marketing lead acquisition and conversion performance using the Olist public marketing funnel dataset. The dashboard helps explore:

- How many marketing-qualified leads became closed deals.
- The overall conversion and lead drop-off rates.
- Lead volume and conversion performance by marketing origin.
- Monthly lead generation based on the first contact date.
- The business-segment mix among closed deals.
- The relationship between declared product catalogue size and monthly revenue where both values are available.

## Dashboard preview

Open the [live Streamlit dashboard](https://futureds03-khuemcchuralwposb29n6u.streamlit.app/) to explore the interactive charts and filters.

## Key dashboard features

### Executive KPIs

- **Total Marketing Leads** – number of unique marketing-qualified leads in the current selection.
- **Closed Deals** – leads that have a matching record in the closed-deals dataset.
- **Conversion Rate** – percentage of selected leads linked to a closed deal.
- **Lead Drop-off** – percentage of selected leads without a matching closed-deal record.

### Visual analysis

1. **Lead Conversion Funnel** – compares marketing-qualified leads with closed deals.
2. **Leads by Marketing Origin** – donut chart showing the distribution of leads across acquisition origins.
3. **Monthly Lead Generation** – shows lead volume by first contact month.
4. **Closed Deals by Business Segment** – treemap showing the segment distribution of closed deals.
5. **Catalog Size vs Monthly Revenue** – scatter plot for closed deals with complete positive values; revenue is displayed on a logarithmic scale.
6. **Conversion Rate by Marketing Origin** – compares the conversion rate across recorded origins.

### Interactive filters

The sidebar provides filters for:

- Marketing origin
- First contact period
- Business segment
- Lead type
- Business type

The dashboard also includes a **Reset all filters** option. Lead-level filters update the overall funnel and KPIs. Business segment, lead type and business type filters apply to the closed-deal analysis because these attributes are recorded in the closed-deals dataset.

### Findings and recommendations

The dashboard includes dynamically updated **Key Business Insights**, **Project Findings**, and **Recommendations**. These sections are based on the selected data and highlight channel performance, lead-source attribution gaps, the lead-to-deal gap and the closed-deal segment mix.

---

## Dataset

This project uses the publicly available **Olist Marketing Funnel** dataset from Kaggle. It contains two CSV files:

| File | Description |
|---|---|
| `olist_marketing_qualified_leads_dataset.csv` | Marketing-qualified lead records, including lead ID, first contact date, landing page ID and marketing origin. |
| `olist_closed_deals_dataset.csv` | Closed-deal records, including lead ID, deal date and available business/customer attributes. |

The two datasets are connected using the `mql_id` field.

**Note:** The dataset is a public Olist dataset downloaded from Kaggle. It is not represented as a dataset provided by Future Interns.

## Tools and technologies

- **Python** – data analysis and dashboard logic
- **Pandas** – data loading, cleaning, merging and aggregation
- **NumPy** – conversion-status calculations
- **Plotly Express / Plotly Graph Objects** – interactive charts
- **Streamlit** – interactive web dashboard
- **GitHub** – project version control and source code hosting
- **Streamlit Community Cloud** – dashboard deployment

## Project workflow

1. **Load the data** – read the marketing-qualified leads and closed-deals CSV files.
2. **Clean the data** – convert date columns, standardise marketing-origin values and prepare numeric fields.
3. **Merge datasets** – join the two datasets using `mql_id`.
4. **Identify conversion status** – classify a lead as converted when a matching closed-deal record exists.
5. **Calculate KPIs** – calculate total leads, closed deals, conversion rate and lead drop-off.
6. **Analyse marketing origins** – compare lead volume and conversion rates across origins.
7. **Explore closed deals** – analyse business segments and available catalogue/revenue information.
8. **Build the dashboard** – create interactive Plotly visualisations and Streamlit sidebar filters.
9. **Generate findings and recommendations** – translate the selected results into practical business observations and actions.

## Repository structure

```
FUTURE_DS_03/
│
├── app.py
├── olist_marketing_qualified_leads_dataset.csv
├── olist_closed_deals_dataset.csv
└── README.md
```

## Run the project locally

### 1. Clone the repository

```bash
git clone https://github.com/Aryan18-03/FUTURE_DS_03.git
cd FUTURE_DS_03
```

### 2. Install the required libraries

Make sure Python is installed, then run:

```bash
pip install streamlit pandas numpy plotly
```

### 3. Start the Streamlit dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal, usually:

```
http://localhost:8501
```

Keep both dataset CSV files in the same folder as `app.py`.

## Key results from the full dataset

The following figures describe the full dataset before applying dashboard filters:

| Metric | Result |
|---|---:|
| Marketing-qualified leads | 8,000 |
| Leads linked to closed deals | 842 |
| Leads without a matching closed-deal record | 7,158 |
| Overall conversion rate | 10.53% |
| Lead drop-off | 89.48% |

These are descriptive results from the available records. A lead without a matching closed-deal record is counted as not converted for this analysis; the dataset alone does not explain why that lead did not become a customer.

## Important analysis notes

- **Unknown marketing origin:** missing origin values are labelled as unknown/unattributed. They are not treated as a named marketing channel when identifying the strongest known channel.
- **Closed-deal attributes:** business segment, lead type and business type are available in the closed-deals data. Their filters therefore affect closed-deal charts, not the overall lead population.
- **Segment interpretation:** the business-segment chart describes the distribution of closed deals. It does not represent segment-level conversion rates.
- **Scatter plot coverage:** the catalogue-size/revenue chart uses only closed-deal records with complete, positive values for both fields.
- **Monthly trend:** monthly lead generation is grouped by `first_contact_date`; it is not a monthly closed-deal or cohort-conversion trend.
- **Conversion definition:** conversion is identified by matching `mql_id` values between the marketing-qualified leads and closed-deals datasets.

## Author

**Aryan**  
Aspiring Data Analyst | Python | SQL | Excel | Power BI | Tableau

- [GitHub](https://github.com/Aryan18-03)
- [LinkedIn](https://www.linkedin.com/in/aryan-data-analyst183/)

---

*Created as part of Future Interns – Data Science & Analytics Task 3.*
