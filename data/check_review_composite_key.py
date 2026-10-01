import pandas as pd

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

print("=" * 60)
print("REVIEW COMPOSITE KEY VALIDATION")
print("=" * 60)

# Check whether the combination is unique
duplicate_pairs = reviews.duplicated(
    subset=["review_id", "order_id"],
    keep=False
)

print("Total records:", len(reviews))
print(
    "Unique review_id + order_id combinations:",
    reviews.drop_duplicates(
        subset=["review_id", "order_id"]
    ).shape[0]
)

print(
    "Duplicate combinations:",
    duplicate_pairs.sum()
)

if duplicate_pairs.sum() == 0:
    print("\n[PASS] Composite key is unique.")
else:
    print("\n[FAIL] Composite key contains duplicates.")

    print(
        reviews[duplicate_pairs]
        .sort_values(["review_id", "order_id"])
        .to_string(index=False)
    )

print("=" * 60)