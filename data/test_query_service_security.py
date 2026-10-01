from backend.database.query_service import execute_query


unsafe_queries = {
    "DELETE query": "DELETE FROM analytics.customers;",
    "UPDATE query": "UPDATE analytics.customers SET customer_city = 'Test';",
    "Raw schema query": "SELECT * FROM raw.customers;",
    "Multiple statements": "SELECT * FROM analytics.orders; SELECT * FROM analytics.customers;"
}


for name, query in unsafe_queries.items():
    try:
        execute_query(query)
        print(f"{name}: FAILED — Query was executed.")

    except ValueError as error:
        print(f"{name}: BLOCKED — {error}")