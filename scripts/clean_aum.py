import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/03_aum_by_fund_house.csv")

print("Original Shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert numeric columns
df["aum_lakh_crore"] = pd.to_numeric(df["aum_lakh_crore"], errors="coerce")
df["aum_crore"] = pd.to_numeric(df["aum_crore"], errors="coerce")
df["num_schemes"] = pd.to_numeric(df["num_schemes"], errors="coerce")

# Remove rows with invalid dates
df = df.dropna(subset=["date"])

# Keep only valid positive values
df = df[
    (df["aum_lakh_crore"] > 0) &
    (df["aum_crore"] > 0) &
    (df["num_schemes"] > 0)
]

# Save cleaned dataset
df.to_csv("data/processed/03_aum_by_fund_house_clean.csv", index=False)

print("Cleaned Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nAUM dataset cleaned successfully!")