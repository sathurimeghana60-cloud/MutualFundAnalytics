import pandas as pd

fund = pd.read_csv("data/raw/01_fund_master.csv")
nav = pd.read_csv("data/raw/02_nav_history.csv")

fund_codes = set(fund["amfi_code"])
nav_codes = set(nav["amfi_code"])

missing = fund_codes - nav_codes

print("Total Fund Master Codes :", len(fund_codes))
print("Total NAV History Codes :", len(nav_codes))
print("Missing Codes :", missing)

if len(missing) == 0:
    print("\n✅ All AMFI codes in fund_master exist in nav_history.")
else:
    print(f"\n❌ {len(missing)} AMFI codes are missing.")