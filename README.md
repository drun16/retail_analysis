# ABC Retail Solutions - End-to-End Data Engineering Pipeline

## 📌 Project Overview
[cite_start]ABC Retail Solutions requires a robust and standardized data pipeline to analyze transactional retail data collected from multiple online and offline channels[cite: 3, 4]. [cite_start]The raw datasets suffer from several data quality issues, including duplicate records, inconsistent date formats, missing prices, and unstandardized categorical values[cite: 4, 19]. 

[cite_start]This project implements an end-to-end data engineering pipeline using **PySpark** to ingest, clean, transform, and aggregate the raw data, followed by a **Power BI** dashboard to generate actionable business insights[cite: 6, 40]. [cite_start]PySpark was selected as the core processing engine to ensure the architecture remains highly scalable for future, larger retail datasets[cite: 73, 89].

---

## 🏗️ Repository Structure
[cite_start]As per the project requirements, the repository is organized into the following subfolders[cite: 51]:

* **`Code/`**: Contains the complete data pipeline logic. [cite_start]Includes the `pipeline.py` script (converted from the original Jupyter Notebook) which handles data ingestion, transformation, PII masking, and aggregation[cite: 52, 53, 56].
* [cite_start]**`Documentation/`**: Contains the detailed project documentation (`.docx`), detailing the architecture diagram, data flow, assumptions, data cleaning strategies, and transformation logic[cite: 54, 60, 61].
* [cite_start]**`Power BI/`**: Contains the Power BI report file (`.pbix`) and screenshots of the interactive dashboard featuring insights on Revenue Analysis, Product Performance, Category Trends, and Regional Insights[cite: 43, 55, 59].
* **`data/`** *(Optional/Gitignored)*: Recommended local folder for storing `retail_data1.csv`, `retail_data2.csv`, and `product_details.csv`. 

---

## ⚙️ Data Pipeline Workflow

The PySpark ETL (Extract, Transform, Load) process follows these distinct phases:

### 1. Data Ingestion
* [cite_start]Loaded two transactional datasets (`retail_data1`, `retail_data2`) comprising over 8,400 records[cite: 14, 15, 17, 18].
* [cite_start]Loaded the `product_details` dimension table (10 standardized records) for data enrichment[cite: 10, 11].

### 2. Data Transformation & Cleaning
* [cite_start]**Union & Deduplication:** Merged both transaction datasets and dropped exact duplicate records to ensure data integrity[cite: 20, 29].
* [cite_start]**Standardization:** Resolved varying date formats into a standard `YYYY-MM-DD` structure[cite: 4]. [cite_start]Handled invalid quantities and inconsistent naming conventions[cite: 4].
* [cite_start]**Data Enrichment:** Joined the transaction table with the `product_details` dimension table to handle missing prices and validate product categories[cite: 12, 13, 29].
* [cite_start]**Data Governance (PII Masking):** Implemented SHA-256 hashing on sensitive Personally Identifiable Information (PII) columns, specifically customer email addresses and phone numbers, to ensure compliance with data protection standards[cite: 20, 30, 31, 93].

### 3. Data Aggregation
[cite_start]The cleaned dataset was aggregated to calculate key business metrics, including[cite: 32, 34]:
* [cite_start]Total Revenue [cite: 35]
* [cite_start]Revenue by Category [cite: 36]
* [cite_start]Revenue by City [cite: 37]

---

## 📊 Business Intelligence Dashboard
[cite_start]The curated data was loaded into **Power BI** to create an interactive dashboard[cite: 39, 40]. [cite_start]The report is divided into logical sections and includes interactive filters, slicers, and KPI cards to support data-driven decision-making[cite: 41, 42]. 

*Key visualizations include:*
* High-level KPI cards for Total Revenue and Order Volume.
* Category performance breakdowns.
* Regional insights mapped by City.

---

## 🚀 Setup & Execution Instructions

To run the PySpark pipeline locally:

1. **Prerequisites:** Ensure you have Python 3.8+ and Java (required for Spark) installed on your system.
2. **Install Dependencies:**
   ```bash
   pip install pyspark pandas