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
        .insights-header {
            margin-top: 1.25rem;
            margin-bottom: 0.75rem;
            padding: 0.95rem 1.1rem;
            border-left: 5px solid #D7263D;
            border-radius: 0 12px 12px 0;
            background: linear-gradient(
                90deg,
                rgba(90,24,154,0.14),
                rgba(215,38,61,0.06)
            );
        }
        .insights-kicker {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            color: #F4D35E;
            margin-bottom: 0.2rem;
        }
        .insights-title {
            font-size: 1.45rem;
            font-weight: 700;
            margin: 0;
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

month_names = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

month_order = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


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

selected_category = st.sidebar.selectbox("Category", ["All", "Men's", "Women's"])

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

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["PRODUCT_NAME"].str.startswith(selected_category)
    ]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["STATE"] == selected_state]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["PRODUCT_NAME"] == selected_product]

if filtered_df.empty:
    st.warning("No sales records match the selected filters.")
    st.stop()


# -----------------------------
# Executive insights
# -----------------------------
st.markdown(
    """
    <div class="insights-header">
        <div class="insights-kicker">EXECUTIVE INSIGHTS</div>
        <div class="insights-title">What stands out in the current view</div>
    </div>
    """,
    unsafe_allow_html=True
)

product_insight = (
    filtered_df.dropna(subset=["PRODUCT_NAME"])
    .groupby("PRODUCT_NAME")["SALES_DOLLARS"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_insight.index[0] if len(product_insight) > 0 else "N/A"
top_product_sales = product_insight.iloc[0] if len(product_insight) > 0 else 0

state_insight = (
    filtered_df.dropna(subset=["STATE"])
    .groupby("STATE")["SALES_DOLLARS"]
    .sum()
    .sort_values(ascending=False)
)

top_state = state_insight.index[0] if len(state_insight) > 0 else "N/A"
top_state_sales = state_insight.iloc[0] if len(state_insight) > 0 else 0

retailer_insight = (
    filtered_df.dropna(subset=["RETAILER"])
    .groupby("RETAILER")["UNITS_SOLD"]
    .sum()
    .sort_values(ascending=False)
)

top_retailer = retailer_insight.index[0] if len(retailer_insight) > 0 else "N/A"
top_retailer_units = retailer_insight.iloc[0] if len(retailer_insight) > 0 else 0

month_insight = (
    filtered_df.dropna(subset=["MONTH"])
    .groupby("MONTH")["SALES_DOLLARS"]
    .sum()
    .sort_values(ascending=False)
)

if len(month_insight) > 0:
    peak_month_number = int(month_insight.index[0])
    peak_month = month_names.get(peak_month_number, str(peak_month_number))
    peak_month_sales = month_insight.iloc[0]
else:
    peak_month = "N/A"
    peak_month_sales = 0

insight1, insight2, insight3, insight4 = st.columns(4)

insight1.metric(
    "Top Product",
    top_product,
    help=f"${top_product_sales:,.0f} in sales for the current filters"
)

insight2.metric(
    "Top State",
    top_state,
    help=f"${top_state_sales:,.0f} in sales for the current filters"
)

insight3.metric(
    "Top Retailer by Units",
    top_retailer,
    help=f"{top_retailer_units:,.0f} units for the current filters"
)

insight4.metric(
    "Peak Sales Month",
    peak_month,
    help=f"${peak_month_sales:,.0f} in sales for the current filters"
)

unresolved_state_count = int(filtered_df["STATE"].isna().sum())
unresolved_retailer_count = int(filtered_df["RETAILER"].isna().sum())

if unresolved_state_count > 0 or unresolved_retailer_count > 0:
    st.caption(
        f"Data note: location-based insights exclude {unresolved_state_count:,} "
        f"transaction(s) with unresolved state; retailer rankings exclude "
        f"{unresolved_retailer_count:,} transaction(s) with unresolved retailer."
    )

st.divider()


# -----------------------------
# KPI cards
# -----------------------------
total_sales = filtered_df["SALES_DOLLARS"].sum()
total_units = filtered_df["UNITS_SOLD"].sum()
total_orders = filtered_df["ORDER_ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Units Sold", f"{total_units:,.0f}")
col3.metric("Orders", f"{total_orders:,.0f}")


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

st.plotly_chart(fig_map, width="stretch")


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

    fig_products.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>"
    )
    fig_products.update_layout(showlegend=False)
    st.plotly_chart(fig_products, width="stretch")


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

    monthly_sales["MONTH_NAME"] = (
        monthly_sales["MONTH"].astype(int).map(month_names)
    )

    fig_month = px.line(
        monthly_sales,
        x="MONTH_NAME",
        y="SALES_DOLLARS",
        markers=True,
        category_orders={"MONTH_NAME": month_order},
        labels={
            "MONTH_NAME": "Month",
            "SALES_DOLLARS": "Sales Dollars"
        }
    )

    fig_month.update_traces(
        line_color="#D7263D",
        marker_color="#F4D35E",
        marker_size=8,
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )

    st.plotly_chart(fig_month, width="stretch")


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
    width="stretch",
    hide_index=True,
    column_config={
        "Sales": st.column_config.NumberColumn("Sales", format="$%,.0f"),
        "Units": st.column_config.NumberColumn("Units", format="%,.0f")
    }
)
