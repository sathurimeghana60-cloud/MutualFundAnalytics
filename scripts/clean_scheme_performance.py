import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Original Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert all possible numeric columns
numeric_columns = [
    "return_1y",
    "return_3y",
    "return_5y",
    "expense_ratio"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Check expense ratio range
if "expense_ratio" in df.columns:
    anomalies = df[
        (df["expense_ratio"] < 0.1) |
        (df["expense_ratio"] > 2.5)
    ]

    print("\nExpense Ratio Anomalies:")
    print(anomalies)

# Remove completely empty rows
df = df.dropna(how="all")

# Save cleaned dataset
output = "data/processed/07_scheme_performance_clean.csv"
df.to_csv(output, index=False)

print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nScheme Performance cleaned successfully!")
print("Saved to:", output)