import pandas as pd

# Load reviews dataset
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

print("=" * 65)
print("REVIEW ID INVESTIGATION")
print("=" * 65)

# 1. Count repeated review IDs
duplicate_mask = reviews["review_id"].duplicated(keep=False)
duplicate_records = reviews[duplicate_mask].sort_values("review_id")

print("\n1. DUPLICATE REVIEW ID SUMMARY")
print("-" * 65)

print("Total review records:", len(reviews))
print("Unique review IDs:", reviews["review_id"].nunique())
print("Rows with repeated IDs:", duplicate_mask.sum())
print(
    "Distinct IDs that repeat:",
    duplicate_records["review_id"].nunique()
)

# 2. Display sample repeated IDs
print("\n2. SAMPLE REPEATED REVIEW RECORDS")
print("-" * 65)

print(
    duplicate_records[
        [
            "review_id",
            "order_id",
            "review_score",
            "review_creation_date",
            "review_answer_timestamp"
        ]
    ].head(20).to_string(index=False)
)

# 3. Check whether repeated IDs map to multiple orders
print("\n3. REVIEW ID TO ORDER RELATIONSHIP")
print("-" * 65)

orders_per_review = (
    duplicate_records.groupby("review_id")["order_id"].nunique()
)

print(
    "Repeated review IDs linked to multiple orders:",
    (orders_per_review > 1).sum()
)

print(
    "Repeated review IDs linked to one order:",
    (orders_per_review == 1).sum()
)

# 4. Check which columns differ within repeated IDs
print("\n4. COLUMN VARIATION")
print("-" * 65)

variation = (
    duplicate_records.groupby("review_id")
    .nunique()
)

for column in reviews.columns:
    if column != "review_id":
        print(
            f"{column}: "
            f"{(variation[column] > 1).sum()} repeated IDs "
            "have different values"
        )

print("\n" + "=" * 65)
print("INVESTIGATION COMPLETED")
print("=" * 65)