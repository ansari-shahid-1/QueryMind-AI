
from pathlib import Path
import pandas as pd

# Locate the raw dataset directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

print("=" * 60)
print("       QUERYMIND AI - DATASET INSPECTION")
print("=" * 60)

# Find all CSV files
csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("No CSV files found. Please check the data/raw directory.")
else:
    print(f"\nTotal CSV files found: {len(csv_files)}")

    for file_path in csv_files:
        print("\n" + "-" * 60)
        print(f"FILE: {file_path.name}")
        print("-" * 60)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Basic information
        print(f"Rows: {df.shape[0]:,}")
        print(f"Columns: {df.shape[1]}")

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nData types:")
        print(df.dtypes)

        print("\nMissing values:")
        missing = df.isnull().sum()
        print(missing[missing > 0] if missing.any() else "No missing values")

        print("\nFirst 3 records:")
        print(df.head(3).to_string(index=False))

print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETED")
print("=" * 60)