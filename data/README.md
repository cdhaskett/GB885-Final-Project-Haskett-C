# RUSH Sales Data

This folder contains the raw and cleaned data used for the RUSH sales analysis project.

## Data Tables

### TABLE_SALES_885.csv
The main transaction-level sales table.

Important fields include:
- Order ID
- Invoice date
- Product ID
- Retailer ID
- Price per unit
- Units sold
- Operating margin
- Sales method

This table is used as the primary fact table for the analysis.

### TABLE_PRODUCTS_885.csv
Contains product information used to identify the products associated with each sales transaction.

Important fields include:
- Product ID
- Product name/category

The Product ID is used to connect this table to the sales table.

### TABLE_RETAILER_885.csv
Contains retailer and geographic information.

Important fields include:
- Retailer ID
- Retailer name
- Region
- State
- City

During data cleaning, several duplicate Retailer IDs were identified and investigated before the retailer data was merged with the sales table.

### rush_cleaned_sales.csv
The cleaned and merged dataset created during the analysis.

This file combines sales, product, and retailer information and includes calculated fields such as total sales dollars. It is used as the data source for the interactive Streamlit dashboard.

## Data Cleaning Notes

The original data contained several retailer ID collisions where the same ID was assigned to more than one retailer-location combination. These records were investigated and corrected where the available data supported a reliable assignment.

Records that could not be confidently assigned were left unresolved rather than being assigned arbitrarily.
