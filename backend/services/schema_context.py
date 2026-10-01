from backend.database.connection import get_connection


TABLE_RELATIONSHIPS = [
    "orders.customer_id = customers.customer_id",
    "order_items.order_id = orders.order_id",
    "order_items.product_id = products.product_id",
    "order_items.seller_id = sellers.seller_id",
    "payments.order_id = orders.order_id",
    "order_reviews.order_id = orders.order_id",
    "products.product_category_name = category_translation.product_category_name",
]


ANALYTICAL_NOTES = [
    "Use order_items.price for item-level sales value.",
    "Use payments.payment_value for payment amounts.",
    "Do not directly add order_items.price and payments.payment_value.",
    "An order can contain multiple items and multiple payment records.",
    "Joining order_items with payments on order_id can multiply rows.",
    "Use COUNT(DISTINCT orders.order_id) when counting orders after joining order_items.",
    "Geolocation ZIP prefixes are not unique.",
    "order_reviews.review_id is not unique; use review_record_id to identify individual review records.",
]


def get_schema_context():
    query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'analytics'
        ORDER BY table_name, ordinal_position;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = cur.fetchall()

    schema = {}

    for table_name, column_name, data_type in columns:
        schema.setdefault(table_name, []).append(
            f"{column_name} ({data_type})"
        )

    context = ["Database schema: analytics"]

    for table_name, table_columns in schema.items():
        context.append(f"\nTable: analytics.{table_name}")

        for column in table_columns:
            context.append(f"- {column}")

    context.append("\nTable relationships:")

    for relationship in TABLE_RELATIONSHIPS:
        context.append(f"- {relationship}")

    context.append("\nAnalytical notes:")

    for note in ANALYTICAL_NOTES:
        context.append(f"- {note}")

    return "\n".join(context)