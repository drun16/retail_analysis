import pandas as pd
import hashlib
import numpy as np

print("Starting ABC Retail Data Pipeline (Pandas)...\n")

# ---------------------------------------------------------
# 1. DATA INGESTION
# ---------------------------------------------------------
print("Ingesting data...")
try:
    df_retail1 = pd.read_csv('../data/retail_data1.csv')
    df_retail2 = pd.read_csv('../data/retail_data2.csv')
    df_products = pd.read_csv('../data/product_details.csv')
    print(f"Loaded: retail_data1 ({len(df_retail1)} rows), retail_data2 ({len(df_retail2)} rows)")
except FileNotFoundError:
    print("Error: Could not find the CSV files. Please ensure you ran the data generator first.")
    exit()

# ---------------------------------------------------------
# 2. DATA TRANSFORMATION AND CLEANING
# ---------------------------------------------------------
print("\nTransforming and cleaning data...")

# A. Union the datasets
df_combined = pd.concat([df_retail1, df_retail2], ignore_index=True)
print(f"Total rows after union: {len(df_combined)}")

# B. Deduplication
df_combined.drop_duplicates(subset=['Transaction ID'], keep='first', inplace=True)
print(f"Total rows after removing duplicates: {len(df_combined)}")

# C. Standardize Dates
# Converts varying formats (MM/DD/YYYY or YYYY-MM-DD) to a standard datetime format
df_combined['Transaction Date'] = pd.to_datetime(df_combined['Transaction Date'], format='mixed').dt.strftime('%Y-%m-%d')

# D. Handle Invalid Quantities
# Replace negative or zero quantities with a default of 1 (or drop them depending on business rules)
df_combined['Quantity'] = df_combined['Quantity'].apply(lambda x: x if x > 0 else 1)

# E. Standardize Text (Cities)
df_combined['City'] = df_combined['City'].str.title()

# ---------------------------------------------------------
# 3. PII MASKING (Data Governance)
# ---------------------------------------------------------
print("\nApplying PII Masking...")

def hash_pii(value):
    if pd.isna(value):
        return value
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

df_combined['Customer Email'] = df_combined['Customer Email'].apply(hash_pii)
df_combined['Customer Phone'] = df_combined['Customer Phone'].apply(hash_pii)

# ---------------------------------------------------------
# 4. DATA ENRICHMENT & AGGREGATION
# ---------------------------------------------------------
print("\nEnriching data and calculating KPIs...")

# A. Join with Product Details to get missing information
df_final = pd.merge(df_combined, df_products, on='Product ID', how='left')

# B. Handle Missing Prices
# If the transaction price is missing, fill it with the standard product price
df_final['Price'] = df_final['Price'].fillna(df_final['Standard Product Price'])

# C. Calculate Total Revenue KPI per row
df_final['Total Revenue'] = df_final['Quantity'] * df_final['Price']

# ---------------------------------------------------------
# 5. EXPORT
# ---------------------------------------------------------
output_path = '../data/Gold_Cleaned_Retail_Data.csv'
df_final.to_csv(output_path, index=False)
print(f"\nPipeline execution complete! Cleaned dataset saved to: {output_path}")