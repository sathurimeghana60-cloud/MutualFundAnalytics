import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/08_investor_transactions.csv")

print("Original Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Remove duplicates
df = df.drop_duplicates()

# Standardize transaction type
if "transaction_type" in df.columns:
    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    transaction_mapping = {
        "sip": "SIP",
        "lumpsum": "Lumpsum",
        "lump sum": "Lumpsum",
        "redemption": "Redemption"
    }

    df["transaction_type"] = (
        df["transaction_type"]
        .map(transaction_mapping)
        .fillna(df["transaction_type"])
    )

# Validate amount
if "amount" in df.columns:
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]

# Fix date format
if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )
    df = df.dropna(subset=["date"])

# Check KYC status
if "kyc_status" in df.columns:
    valid_kyc = ["Verified", "Pending", "Rejected"]

    invalid_kyc = df[
        ~df["kyc_status"].isin(valid_kyc)
    ]

    print("\nInvalid KYC Status Values:")
    print(invalid_kyc["kyc_status"].unique())

# Save cleaned dataset
output = "data/processed/08_investor_transactions_clean.csv"
df.to_csv(output, index=False)

print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nInvestor Transactions cleaned successfully!")
print("Saved to:", output)