
import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg import sql


load_dotenv()

TABLES = [
    "customers",
    "orders",
    "order_items",
    "payments",
    "order_reviews",
    "products",
    "sellers",
    "geolocation",
    "category_translation",
]

OUTPUT_DIR = Path(__file__).parent / "processed"
OUTPUT_FILE = OUTPUT_DIR / "missing_values_report.csv"


def profile_table(cur, table):
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'raw'
          AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )

    columns = [row[0] for row in cur.fetchall()]

    checks = [
        sql.SQL(
            "COUNT(*) FILTER (WHERE {} IS NULL OR BTRIM({}) = '')"
        ).format(sql.Identifier(column), sql.Identifier(column))
        for column in columns
    ]

    query = sql.SQL(
        "SELECT COUNT(*), {} FROM raw.{}"
    ).format(
        sql.SQL(", ").join(checks),
        sql.Identifier(table),
    )

    cur.execute(query)
    result = cur.fetchone()

    total_rows = result[0]

    report = []

    for column, missing_count in zip(columns, result[1:]):
        report.append({
            "table_name": table,
            "column_name": column,
            "total_rows": total_rows,
            "missing_values": missing_count,
            "missing_percentage": round(
                (missing_count / total_rows) * 100, 2
            ) if total_rows else 0,
        })

    return report


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_results = []

    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:

        with conn.cursor() as cur:
            for table in TABLES:
                print(f"Profiling raw.{table}...")

                results = profile_table(cur, table)
                all_results.extend(results)

                missing_columns = [
                    item for item in results
                    if item["missing_values"] > 0
                ]

                if missing_columns:
                    for item in missing_columns:
                        print(
                            f"  {item['column_name']}: "
                            f"{item['missing_values']:,} missing "
                            f"({item['missing_percentage']}%)"
                        )
                else:
                    print("  No missing values found.")

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "table_name",
                "column_name",
                "total_rows",
                "missing_values",
                "missing_percentage",
            ],
        )
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nReport saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()