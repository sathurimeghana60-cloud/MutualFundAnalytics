import os
import requests
import pandas as pd

# Create data/raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        print("\n--------------------------------------")
        print("Fund Name :", data["meta"]["scheme_name"])
        print("Fund House:", data["meta"]["fund_house"])

        df = pd.DataFrame(data["data"])

        file_name = f"data/raw/{name}.csv"
        df.to_csv(file_name, index=False)

        print(f"Saved as {file_name}")

    else:
        print(f"Failed to fetch scheme {code}")