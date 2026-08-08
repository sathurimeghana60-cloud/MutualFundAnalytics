import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/06_industry_folio_count.csv")

print("Original Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date/month column if present
if "month" in df.columns:
    df["month"] = pd.to_datetime(
        df["month"],
        errors="coerce"
    )

if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

# Convert numeric columns
numeric_columns = [
    "folio_count",
    "folio_count_crore",
    "number_of_folios",
    "num_folios"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Folio counts cannot be negative
        df = df[df[col] >= 0]

# Remove rows with invalid dates
if "month" in df.columns:
    df = df.dropna(subset=["month"])

if "date" in df.columns:
    df = df.dropna(subset=["date"])

# Remove completely empty rows
df = df.dropna(how="all")

# Save cleaned dataset
output = "data/processed/06_industry_folio_count_clean.csv"
df.to_csv(output, index=False)

print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nIndustry Folio Count cleaned successfully!")
print("Saved to:", output)