from backend.services.sql_validator import validate_query


test_queries = {
    "Safe query": """
        SELECT COUNT(*)
        FROM analytics.customers;
    """,

    "Delete query": """
        DELETE FROM analytics.customers;
    """,

    "Update query": """
        UPDATE analytics.customers
        SET customer_city = 'Test';
    """,

    "Raw schema query": """
        SELECT *
        FROM raw.customers;
    """,

    "Multiple statements": """
        SELECT * FROM analytics.orders;
        SELECT * FROM analytics.customers;
    """,

    "Invalid SQL": """
        SELEC * FROM analytics.orders;
    """,

    "Unapproved table": """
        SELECT *
        FROM analytics.unknown_table;
    """,

    "Prohibited function - pg_sleep": """
        SELECT pg_sleep(5);
    """,

    "Prohibited function - set_config": """
        SELECT set_config('statement_timeout', '0', false);
    """,

    "SELECT INTO": """
        SELECT customer_id
        INTO analytics.test_table
        FROM analytics.customers;
    """,

    "Valid aggregation": """
        SELECT order_status, COUNT(*)
        FROM analytics.orders
        GROUP BY order_status;
    """
}


for name, query in test_queries.items():
    is_valid, message = validate_query(query)

    print(f"{name}: {'ACCEPTED' if is_valid else 'REJECTED'}")
    print(f"Reason: {message}\n")