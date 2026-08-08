import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/10_benchmark_indices.csv")

print("Original Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Remove duplicates
df = df.drop_duplicates()

# Convert possible date columns
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

if "month" in df.columns:
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.dropna(subset=["month"])

# Convert possible numeric columns
numeric_columns = [
    "index_value",
    "value",
    "close",
    "open",
    "high",
    "low",
    "return_pct"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate index values
for col in ["index_value", "value", "close"]:
    if col in df.columns:
        df = df[df[col] > 0]

# Remove completely empty rows
df = df.dropna(how="all")

# Save cleaned dataset
output = "data/processed/10_benchmark_indices_clean.csv"
df.to_csv(output, index=False)

print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nBenchmark Indices cleaned successfully!")
print("Saved to:", output)