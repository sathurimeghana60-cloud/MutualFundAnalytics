import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/09_portfolio_holdings.csv")

print("Original Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert possible numeric columns
numeric_columns = [
    "holding_pct",
    "weight_pct",
    "percentage",
    "market_value",
    "shares",
    "quantity"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate percentage columns
for col in ["holding_pct", "weight_pct", "percentage"]:
    if col in df.columns:
        df = df[
            (df[col] >= 0) &
            (df[col] <= 100)
        ]

# Remove completely empty rows
df = df.dropna(how="all")

# Save
output = "data/processed/09_portfolio_holdings_clean.csv"
df.to_csv(output, index=False)

print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nPortfolio Holdings cleaned successfully!")
print("Saved to:", output)