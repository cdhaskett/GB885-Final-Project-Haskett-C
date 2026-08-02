import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="RUSH Sales Dashboard",
    page_icon="🏃",
    layout="wide"
)

st.title("RUSH Sales Dashboard")
st.caption("Interactive exploration of RUSH sales by year, state, and product category.")


# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/rush_cleaned_sales.csv")
    df["INVOICE_DATE"] = pd.to_datetime(df["INVOICE_DATE"])
    return df


df = load_data()


# -----------------------------
# State abbreviations for map
# -----------------------------
state_abbreviations = {
    'Alabama':'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR',
    'California':'CA', 'Colorado':'CO', 'Connecticut':'CT',
    'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI',
    'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Iowa':'IA',
    'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME',
    'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI',
    'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO',
    'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV',
    'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM',
    'New York':'NY', 'North Carolina':'NC', 'North Dakota':'ND',
    'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA',
    'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD',
    'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT',
    'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV',
    'Wisconsin':'WI', 'Wyoming':'WY'
}


# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

years = sorted(df["YEAR"].dropna().astype(int).unique())

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

states = sorted(df["STATE"].dropna().unique())

selected_state = st.sidebar.selectbox(
    "State",
    ["All"] + states
)

products = sorted(df["PRODUCT_NAME"].dropna().unique())

selected_product = st.sidebar.selectbox(
    "Product Category",
    ["All"] + products
)


# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["YEAR"] == selected_year
    ]

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["STATE"] == selected_state
    ]

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["PRODUCT_NAME"] == selected_product
    ]


# -----------------------------
# KPI cards
# -----------------------------
total_sales = filtered_df["SALES_DOLLARS"].sum()
total_units = filtered_df["UNITS_SOLD"].sum()

retailer_units = (
    filtered_df.dropna(subset=["RETAILER"])
    .groupby("RETAILER")["UNITS_SOLD"]
    .sum()
)

if len(retailer_units) > 0:
    top_retailer = retailer_units.idxmax()
else:
    top_retailer = "N/A"

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "Units Sold",
    f"{total_units:,.0f}"
)

col3.metric(
    "Top Retailer",
    top_retailer
)


# -----------------------------
# Sales map
# -----------------------------
st.subheader("Sales Concentration by State")

state_sales = (
    filtered_df.dropna(subset=["STATE"])
    .groupby("STATE", as_index=False)["SALES_DOLLARS"]
    .sum()
)

state_sales["STATE_ABBR"] = (
    state_sales["STATE"].map(state_abbreviations)
)

fig_map = px.choropleth(
    state_sales,
    locations="STATE_ABBR",
    locationmode="USA-states",
    color="SALES_DOLLARS",
    scope="usa",
    hover_name="STATE",
    hover_data={
        "SALES_DOLLARS": ":$,.0f",
        "STATE_ABBR": False
    },
    title="Sales by State"
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


# -----------------------------
# Product category chart
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("Sales by Product Category")

    product_sales = (
        filtered_df
        .groupby("PRODUCT_NAME", as_index=False)["SALES_DOLLARS"]
        .sum()
        .sort_values("SALES_DOLLARS")
    )

    fig_products = px.bar(
        product_sales,
        x="SALES_DOLLARS",
        y="PRODUCT_NAME",
        orientation="h",
        labels={
            "SALES_DOLLARS": "Sales Dollars",
            "PRODUCT_NAME": "Product"
        }
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


# -----------------------------
# Monthly trend
# -----------------------------
with right:

    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        filtered_df
        .groupby("MONTH", as_index=False)["SALES_DOLLARS"]
        .sum()
        .sort_values("MONTH")
    )

    fig_month = px.line(
        monthly_sales,
        x="MONTH",
        y="SALES_DOLLARS",
        markers=True,
        labels={
            "MONTH": "Month",
            "SALES_DOLLARS": "Sales Dollars"
        }
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


# -----------------------------
# Top retailers
# -----------------------------
st.subheader("Retailer Performance")

retailer_sales = (
    filtered_df.dropna(subset=["RETAILER"])
    .groupby("RETAILER", as_index=False)
    .agg(
        Sales=("SALES_DOLLARS", "sum"),
        Units=("UNITS_SOLD", "sum")
    )
    .sort_values("Sales", ascending=False)
)

st.dataframe(
    retailer_sales,
    use_container_width=True,
    hide_index=True
)