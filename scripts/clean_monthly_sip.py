import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")

print("Original Shape:", df.shape)

# Convert month to datetime (YYYY-MM)
df["month"] = pd.to_datetime(df["month"], format="%Y-%m", errors="coerce")

# Convert numeric columns
numeric_cols = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove invalid dates
df = df.dropna(subset=["month"])

# Keep only valid positive values
df = df[
    (df["sip_inflow_crore"] > 0) &
    (df["active_sip_accounts_crore"] > 0) &
    (df["new_sip_accounts_lakh"] > 0) &
    (df["sip_aum_lakh_crore"] > 0)
]

# Keep NaN values in yoy_growth_pct
# (Expected for the first few months because YoY cannot be calculated.)

# Save cleaned dataset
df.to_csv(
    "data/processed/04_monthly_sip_inflows_clean.csv",
    index=False
)

print("Cleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nMonthly SIP Inflows cleaned successfully!")