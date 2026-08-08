import sqlite3

DB_PATH = "bluestock_mf.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

print("=" * 50)
print("DATABASE ROW COUNTS")
print("=" * 50)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:25} : {count}")

conn.close()