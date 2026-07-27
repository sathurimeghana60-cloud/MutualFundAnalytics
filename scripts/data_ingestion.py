import os
import pandas as pd

folder = "data/raw"

files = [f for f in os.listdir(folder) if f.endswith(".csv")]

print(f"Found {len(files)} CSV files.\n")

for file in files:
    print("=" * 60)
    print(f"File: {file}")

    path = os.path.join(folder, file)
    df = pd.read_csv(path)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("=" * 60)