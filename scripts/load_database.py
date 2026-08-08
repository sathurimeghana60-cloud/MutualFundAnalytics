import sqlite3
import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "bluestock_mf.db"
PROCESSED = "data/processed"

engine = create_engine(f"sqlite:///{DB_PATH}")

# Create tables
with open("sql/schema.sql", "r", encoding="utf-8") as file:
    schema = file.read()

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(schema)

print("SQLite database and tables created successfully!")

# =========================
# Read cleaned datasets
# =========================

fund = pd.read_csv(f"{PROCESSED}/01_fund_master_clean.csv")
nav = pd.read_csv(f"{PROCESSED}/02_nav_history_clean.csv")
aum = pd.read_csv(f"{PROCESSED}/03_aum_by_fund_house_clean.csv")
transactions = pd.read_csv(
    f"{PROCESSED}/08_investor_transactions_clean.csv"
)
performance = pd.read_csv(
    f"{PROCESSED}/07_scheme_performance_clean.csv"
)

# =========================
# Convert dates
# =========================

fund["launch_date"] = pd.to_datetime(
    fund["launch_date"], errors="coerce"
)

nav["date"] = pd.to_datetime(
    nav["date"], errors="coerce"
)

aum["date"] = pd.to_datetime(
    aum["date"], errors="coerce"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"], errors="coerce"
)

# Performance has no date column, so we don't create date_key for it.
# It is a scheme-level performance snapshot.

# =========================
# DIM FUND
# =========================

fund.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

print("dim_fund loaded:", len(fund))

# =========================
# DIM DATE
# =========================

date_frames = [
    nav[["date"]].rename(columns={"date": "date"}),
    aum[["date"]].rename(columns={"date": "date"}),
    transactions[["transaction_date"]].rename(
        columns={"transaction_date": "date"}
    )
]

dates = pd.concat(date_frames)

dates["date"] = pd.to_datetime(
    dates["date"], errors="coerce"
)

dates = (
    dates.dropna()
    .drop_duplicates()
    .sort_values("date")
)

dates["date_key"] = dates["date"].dt.strftime(
    "%Y%m%d"
).astype(int)

dates["year"] = dates["date"].dt.year
dates["month"] = dates["date"].dt.month
dates["month_name"] = dates["date"].dt.strftime("%B")
dates["quarter"] = dates["date"].dt.quarter

dates = dates[
    [
        "date_key",
        "date",
        "year",
        "month",
        "month_name",
        "quarter"
    ]
]

dates.to_sql(
    "dim_date",
    engine,
    if_exists="replace",
    index=False
)

print("dim_date loaded:", len(dates))

# =========================
# FACT NAV
# =========================

nav["date_key"] = nav["date"].dt.strftime(
    "%Y%m%d"
).astype(int)

nav[
    ["amfi_code", "date_key", "nav"]
].to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

print("fact_nav loaded:", len(nav))

# =========================
# FACT AUM
# =========================

aum["date_key"] = aum["date"].dt.strftime(
    "%Y%m%d"
).astype(int)

aum[
    [
        "date_key",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
].to_sql(
    "fact_aum",
    engine,
    if_exists="replace",
    index=False
)

print("fact_aum loaded:", len(aum))

# =========================
# FACT TRANSACTIONS
# =========================

transactions["date_key"] = (
    transactions["transaction_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

transactions[
    [
        "amfi_code",
        "date_key",
        "transaction_type",
        "amount_inr",
        "state",
        "kyc_status"
    ]
].to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

print(
    "fact_transactions loaded:",
    len(transactions)
)

# =========================
# FACT PERFORMANCE
# =========================

performance[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "expense_ratio_pct"
    ]
].to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

print(
    "fact_performance loaded:",
    len(performance)
)

print("\n===================================")
print("DATABASE LOADING COMPLETED")
print("===================================")