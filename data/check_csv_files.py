from pathlib import Path

data_dir = Path(__file__).parent / "raw"

csv_files = sorted(data_dir.glob("*.csv"))

print(f"CSV files found: {len(csv_files)}\n")

for file in csv_files:
    print(file.name)