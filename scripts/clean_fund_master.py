import os
import pandas as pd

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/01_fund_master.csv")

print("Original Shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing AMFI codes
df = df.dropna(subset=["amfi_code"])

# Standardize text columns
text_columns = ["fund_house", "category", "sub_category", "risk_category"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# Ensure AMFI code is numeric
df["amfi_code"] = pd.to_numeric(df["amfi_code"], errors="coerce")

# Remove invalid AMFI codes
df = df.dropna(subset=["amfi_code"])

# Save cleaned dataset
df.to_csv("data/processed/01_fund_master_clean.csv", index=False)

print("Cleaned Shape:", df.shape)
print("Missing Values:\n", df.isnull().sum())
print("\nFund Master cleaned successfully!")