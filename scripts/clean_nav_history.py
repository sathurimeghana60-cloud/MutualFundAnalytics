import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load data
df = pd.read_csv("data/raw/02_nav_history.csv")

print("Original Shape:", df.shape)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

# Remove rows with invalid dates
df = df.dropna(subset=["date"])

# Convert NAV to numeric
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

# Sort by AMFI code and date
df = df.sort_values(["amfi_code", "date"])

# Forward-fill missing NAV values within each AMFI code
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# Remove duplicates
df = df.drop_duplicates()

# Keep only positive NAV values
df = df[df["nav"] > 0]

# Save cleaned file
df.to_csv("data/processed/02_nav_history_clean.csv", index=False)

print("Cleaned Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nNAV History cleaned successfully!")