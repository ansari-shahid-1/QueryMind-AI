
from pathlib import Path

import psycopg
from dotenv import load_dotenv
import os


load_dotenv()

DATA_DIR = Path(__file__).parent / "raw"

DATASETS = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation",
}


def load_datasets():
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:

        with conn.cursor() as cur:

            # Prevent accidental duplicate imports.
            for table in DATASETS.values():
                cur.execute(f"SELECT COUNT(*) FROM raw.{table}")
                count = cur.fetchone()[0]

                if count > 0:
                    raise RuntimeError(
                        f"raw.{table} already contains {count} rows. "
                        "No data was loaded."
                    )

            for filename, table in DATASETS.items():
                file_path = DATA_DIR / filename

                if not file_path.exists():
                    raise FileNotFoundError(
                        f"Dataset not found: {file_path}"
                    )

                print(f"Loading {filename}...")

                with file_path.open(
                    "r", encoding="utf-8-sig", newline=""
                ) as file:
                    with cur.copy(
                        f"COPY raw.{table} FROM STDIN "
                        "WITH (FORMAT CSV, HEADER TRUE)"
                    ) as copy:
                        copy.write(file.read())

                cur.execute(f"SELECT COUNT(*) FROM raw.{table}")
                count = cur.fetchone()[0]

                print(f"  Loaded {count:,} rows into raw.{table}")

        # The connection context commits if everything succeeds.
        # If an error occurs, the transaction is rolled back.


if __name__ == "__main__":
    load_datasets()
    print("\nAll datasets loaded successfully!")