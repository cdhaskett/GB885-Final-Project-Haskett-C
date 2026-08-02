# RUSH Sales Analysis

This project analyzes sales data for the fictional sportswear company **RUSH**. The goal is to clean and combine multiple business tables, answer a set of management questions, and present the results through both a documented Python analysis and an interactive Streamlit dashboard.

## Business Questions

The analysis is designed to answer the following questions:

1. What product category had the highest sales in dollars in 2021?
2. What state had the highest sales of women's products in 2021?
3. What state had the highest sales of men's products in 2021?
4. What retailer purchased the most units in 2021? In 2020?

The project also explores broader sales patterns by geography, product category, retailer, month, and sales method.

## Project Workflow

The analysis follows a typical data workflow:

- Load the raw data directly from GitHub
- Review table structure, data types, missing values, and key fields
- Investigate duplicate and conflicting retailer IDs
- Create cleaned retailer identifiers where the source data supported a reliable correction
- Preserve unresolved records rather than assigning them arbitrarily
- Merge the sales, product, and retailer tables
- Validate that the merge did not duplicate or remove sales records
- Calculate sales dollars and other analysis fields
- Analyze sales performance and trends
- Export a cleaned dataset for the Streamlit dashboard

## Data

The project uses three source tables:

- `TABLE_SALES_885.csv` — transaction-level sales data
- `TABLE_PRODUCTS_885.csv` — product names and product IDs
- `TABLE_RETAILER_885.csv` — retailer and location information

A cleaned and merged dataset is also included:

- `rush_cleaned_sales.csv`

Additional documentation for the datasets is available in [`data/README.md`](data/README.md).

## Data Quality Notes

During exploratory analysis, several `RETAILER_ID` values that were intended to uniquely identify retailer-location combinations were found to be duplicated across different locations or retailers.

The Walmart and West Gear collisions were investigated using order patterns in the sales data and corrected where the evidence supported a reliable assignment. A group of Sports Direct sales could not be confidently separated between Newark, New Jersey and New York, New York, so those records were intentionally left unresolved rather than assigned arbitrarily.

One additional sales record contained a retailer ID that did not match the retailer table. The transaction was retained for overall sales and product analysis, while its retailer and geographic fields remain unknown.

These decisions are documented in the notebook so the cleaning process remains transparent and reproducible.

## Interactive Dashboard

The Streamlit dashboard provides an interactive way to explore the cleaned data.

Users can filter by:

- Year
- State
- Product category

The dashboard includes:

- Total sales, units sold, and order KPIs
- Executive insight cards
- U.S. sales concentration map
- State hover details with sales, units, and top product
- Product-category sales chart
- Monthly sales trend
- Retailer performance table

The visual design uses a Grateful Dead-inspired color palette while keeping the dashboard presentation focused on the business results.

## Tools Used

- Python
- pandas
- Plotly
- Streamlit
- Google Colab
- GitHub
- GitHub Codespaces

## Repository Structure

```text
GB885-Final-Project-Haskett-C/
│
├── GB885_Final_Project_Haskett_C.ipynb
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    ├── README.md
    ├── TABLE_PRODUCTS_885.csv
    ├── TABLE_RETAILER_885.csv
    ├── TABLE_SALES_885.csv
    └── rush_cleaned_sales.csv
```

## Running the Dashboard

Clone the repository or open it in GitHub Codespaces, then install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python -m streamlit run app.py
```

The dashboard will open in a browser and allow the data to be explored interactively.

## Notebook

The Jupyter notebook contains the full analysis process, including exploratory data analysis, data-quality investigation, cleaning decisions, merge validation, and sales analysis.

Because the raw CSV files are stored in this repository, the notebook can load the source data directly from GitHub instead of requiring manual file uploads.

## Author

**Ciara Haskett**

GB885 Final Project
