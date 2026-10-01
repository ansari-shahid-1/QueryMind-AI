
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_dataset(filename):
    """Load a CSV file from the raw data directory."""
    return pd.read_csv(DATA_DIR / filename)


# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------

customers = load_dataset("olist_customers_dataset.csv")
orders = load_dataset("olist_orders_dataset.csv")
order_items = load_dataset("olist_order_items_dataset.csv")
payments = load_dataset("olist_order_payments_dataset.csv")
reviews = load_dataset("olist_order_reviews_dataset.csv")
products = load_dataset("olist_products_dataset.csv")
sellers = load_dataset("olist_sellers_dataset.csv")


# --------------------------------------------------
# VALIDATION FUNCTIONS
# --------------------------------------------------

def check_unique_key(df, column, table_name):
    """Check whether a column contains unique values."""

    duplicates = df[column].duplicated().sum()

    status = "PASS" if duplicates == 0 else "FAIL"

    print(
        f"[{status}] {table_name}.{column}: "
        f"{duplicates} duplicate values"
    )


def check_composite_key(df, columns, table_name):
    """Check uniqueness across multiple columns."""

    duplicates = df.duplicated(subset=columns).sum()

    status = "PASS" if duplicates == 0 else "FAIL"

    print(
        f"[{status}] {table_name} {columns}: "
        f"{duplicates} duplicate combinations"
    )


def check_foreign_key(child_df, child_column,
                      parent_df, parent_column, relationship):
    """Check whether child keys exist in the parent table."""

    child_values = child_df[child_column].dropna()
    parent_values = set(parent_df[parent_column].dropna())

    invalid = (~child_values.isin(parent_values)).sum()

    status = "PASS" if invalid == 0 else "FAIL"

    print(
        f"[{status}] {relationship}: "
        f"{invalid} unmatched records"
    )


# --------------------------------------------------
# RUN VALIDATION
# --------------------------------------------------

print("\n" + "=" * 65)
print("       QUERYMIND AI - DATA QUALITY REPORT")
print("=" * 65)


# 1. PRIMARY KEY CHECKS

print("\n1. PRIMARY KEY VALIDATION")
print("-" * 65)

check_unique_key(customers, "customer_id", "customers")
check_unique_key(orders, "order_id", "orders")
check_unique_key(products, "product_id", "products")
check_unique_key(sellers, "seller_id", "sellers")
check_unique_key(reviews, "review_id", "reviews")

check_composite_key(
    order_items,
    ["order_id", "order_item_id"],
    "order_items"
)

check_composite_key(
    payments,
    ["order_id", "payment_sequential"],
    "payments"
)


# 2. DUPLICATE ROW CHECKS

print("\n2. DUPLICATE ROW VALIDATION")
print("-" * 65)

datasets = {
    "customers": customers,
    "orders": orders,
    "order_items": order_items,
    "payments": payments,
    "reviews": reviews,
    "products": products,
    "sellers": sellers,
}

for name, df in datasets.items():
    duplicates = df.duplicated().sum()

    print(f"{name}: {duplicates} duplicate rows")


# 3. FOREIGN KEY CHECKS

print("\n3. FOREIGN KEY VALIDATION")
print("-" * 65)

check_foreign_key(
    orders, "customer_id",
    customers, "customer_id",
    "orders -> customers"
)

check_foreign_key(
    order_items, "order_id",
    orders, "order_id",
    "order_items -> orders"
)

check_foreign_key(
    order_items, "product_id",
    products, "product_id",
    "order_items -> products"
)

check_foreign_key(
    order_items, "seller_id",
    sellers, "seller_id",
    "order_items -> sellers"
)

check_foreign_key(
    payments, "order_id",
    orders, "order_id",
    "payments -> orders"
)

check_foreign_key(
    reviews, "order_id",
    orders, "order_id",
    "reviews -> orders"
)


# 4. BUSINESS VALUE CHECKS

print("\n4. BUSINESS VALUE VALIDATION")
print("-" * 65)

print("\nOrder statuses:")
print(orders["order_status"].value_counts(dropna=False))

print("\nReview score distribution:")
print(reviews["review_score"].value_counts(dropna=False).sort_index())

invalid_scores = (
    ~reviews["review_score"].between(1, 5)
).sum()

print(f"\nInvalid review scores: {invalid_scores}")

invalid_prices = (order_items["price"] < 0).sum()

print(f"Negative product prices: {invalid_prices}")


# --------------------------------------------------
# COMPLETION
# --------------------------------------------------

print("\n" + "=" * 65)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 65)