import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("Generating mock retail data...")

# 1. Generate Product Details (Dimension Table)
products = {
    'Product ID': [f'P{str(i).zfill(3)}' for i in range(1, 11)],
    'Product Name': ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Keyboard', 
                     'Mouse', 'Headphones', 'Webcam', 'Printer', 'Router'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Peripherals', 'Peripherals', 
                 'Peripherals', 'Audio', 'Peripherals', 'Office', 'Networking'],
    'Standard Product Price': [1200.0, 800.0, 400.0, 250.0, 50.0, 30.0, 150.0, 80.0, 200.0, 100.0]
}
df_products = pd.DataFrame(products)
df_products.to_csv('../data/product_details.csv', index=False)
print("Created product_details.csv")

# Helper function to generate messy transaction data
def generate_transactions(num_records, start_id, file_num):
    records = []
    cities = ['New York', 'NEW YORK', 'los angeles', 'Chicago', 'Houston', 'HOUSTON']
    
    for i in range(num_records):
        # Intentional Data Quality Issues
        # 1. Varying date formats
        date_obj = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        if random.random() > 0.5:
            date_str = date_obj.strftime("%Y-%m-%d") # YYYY-MM-DD
        else:
            date_str = date_obj.strftime("%m/%d/%Y") # MM/DD/YYYY
            
        # 2. PII Data
        email = f"customer_{random.randint(1000, 9999)}@example.com"
        phone = f"555-{random.randint(1000, 9999)}"
        
        # 3. Missing prices (5% of the time)
        prod_idx = random.randint(0, 9)
        price = products['Standard Product Price'][prod_idx] if random.random() > 0.05 else np.nan
        
        # 4. Invalid quantities (negative or zero)
        quantity = random.randint(1, 5) if random.random() > 0.05 else random.randint(-2, 0)
        
        records.append({
            'Transaction ID': f'T{str(start_id + i).zfill(6)}',
            'Customer Email': email,
            'Customer Phone': phone,
            'Product ID': products['Product ID'][prod_idx],
            'Transaction Date': date_str,
            'Quantity': quantity,
            'Price': price,
            'City': random.choice(cities)
        })
    
    df = pd.DataFrame(records)
    
    # 5. Inject exact duplicates (about 20 rows)
    duplicates = df.sample(20)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    file_path = f'../data/retail_data{file_num}.csv'
    df.to_csv(file_path, index=False)
    print(f"Created retail_data{file_num}.csv with {len(df)} records")

# Generate roughly 4,200 records per file as requested in the assessment
generate_transactions(4243, 1, 1)
generate_transactions(4251, 5000, 2)

print("\nData generation complete! You are ready to run the PySpark pipeline.")