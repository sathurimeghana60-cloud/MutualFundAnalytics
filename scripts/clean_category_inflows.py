import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/05_category_inflows.csv")

print("Original Shape:", df.shape)

# Convert month to datetime
df["month"] = pd.to_datetime(
    df["month"],
    format="%Y-%m",
    errors="coerce"
)

# Convert inflow to numeric
df["net_inflow_crore"] = pd.to_numeric(
    df["net_inflow_crore"],
    errors="coerce"
)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove invalid dates
df = df.dropna(subset=["month"])

# Remove rows where inflow is missing
df = df.dropna(subset=["net_inflow_crore"])

# Standardize category names
df["category"] = df["category"].str.strip()

# Save cleaned dataset
df.to_csv(
    "data/processed/05_category_inflows_clean.csv",
    index=False
)

print("Cleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nCategory Inflows cleaned successfully!")