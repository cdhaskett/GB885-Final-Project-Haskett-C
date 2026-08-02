import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="RUSH Sales Dashboard",
    layout="wide"
)

# Grateful Dead-inspired palette: Scarlet Begonias / Fire on the Mountain
DEAD_COLORS = [
    "#5A189A",  # purple
    "#4361EE",  # blue
    "#00A6A6",  # teal
    "#52B788",  # green
    "#F4D35E",  # gold
    "#F28C28",  # orange
    "#D7263D"   # scarlet
]

DEAD_SCALE = [
    [0.00, "#5A189A"],
    [0.18, "#4361EE"],
    [0.36, "#00A6A6"],
    [0.54, "#52B788"],
    [0.72, "#F4D35E"],
    [0.86, "#F28C28"],
    [1.00, "#D7263D"]
]

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 14px;
            padding: 14px 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
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
selected_year = st.sidebar.selectbox("Year", ["All"] + years)

states = sorted(df["STATE"].dropna().unique())
selected_state = st.sidebar.selectbox("State", ["All"] + states)

products = sorted(df["PRODUCT_NAME"].dropna().unique())
selected_product = st.sidebar.selectbox("Product Category", ["All"] + products)


# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["YEAR"] == selected_year]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["STATE"] == selected_state]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["PRODUCT_NAME"] == selected_product]


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

top_retailer = retailer_units.idxmax() if len(retailer_units) > 0 else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Units Sold", f"{total_units:,.0f}")
col3.metric("Top Retailer", top_retailer)


# -----------------------------
# Sales map
# -----------------------------
st.subheader("Sales Concentration by State")

state_sales = (
    filtered_df.dropna(subset=["STATE"])
    .groupby("STATE", as_index=False)
    .agg(
        SALES_DOLLARS=("SALES_DOLLARS", "sum"),
        UNITS_SOLD=("UNITS_SOLD", "sum")
    )
)

# Find the top product category in each state for the current filters
state_product_sales = (
    filtered_df.dropna(subset=["STATE", "PRODUCT_NAME"])
    .groupby(["STATE", "PRODUCT_NAME"], as_index=False)["SALES_DOLLARS"]
    .sum()
    .sort_values(["STATE", "SALES_DOLLARS"], ascending=[True, False])
    .drop_duplicates("STATE")
    .rename(columns={"PRODUCT_NAME": "TOP_PRODUCT"})
    [["STATE", "TOP_PRODUCT"]]
)

state_sales = state_sales.merge(state_product_sales, on="STATE", how="left")
state_sales["STATE_ABBR"] = state_sales["STATE"].map(state_abbreviations)

fig_map = px.choropleth(
    state_sales,
    locations="STATE_ABBR",
    locationmode="USA-states",
    color="SALES_DOLLARS",
    scope="usa",
    color_continuous_scale=DEAD_SCALE,
    custom_data=["STATE", "SALES_DOLLARS", "UNITS_SOLD", "TOP_PRODUCT"],
    title="Sales by State"
)

# Clean hover popup instead of Plotly's default field labels
fig_map.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Sales: $%{customdata[1]:,.0f}<br>"
        "Units sold: %{customdata[2]:,.0f}<br>"
        "Top product: %{customdata[3]}"
        "<extra></extra>"
    ),
    marker_line_color="rgba(255,255,255,0.55)",
    marker_line_width=0.7
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=55, b=0),
    coloraxis_colorbar=dict(
        title="Sales",
        tickprefix="$",
        tickformat="~s"
    ),
    hoverlabel=dict(
        bgcolor="#171321",
        bordercolor="#F4D35E",
        font_color="white",
        font_size=14
    )
)

st.plotly_chart(fig_map, use_container_width=True)


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
        color="PRODUCT_NAME",
        color_discrete_sequence=DEAD_COLORS,
        labels={
            "SALES_DOLLARS": "Sales Dollars",
            "PRODUCT_NAME": "Product"
        }
    )

    fig_products.update_layout(showlegend=False)
    st.plotly_chart(fig_products, use_container_width=True)


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

    fig_month.update_traces(
        line_color="#D7263D",
        marker_color="#F4D35E",
        marker_size=8,
        hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"
    )

    st.plotly_chart(fig_month, use_container_width=True)


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
    hide_index=True,
    column_config={
        "Sales": st.column_config.NumberColumn("Sales", format="$%,.0f"),
        "Units": st.column_config.NumberColumn("Units", format="%,.0f")
    }
)
