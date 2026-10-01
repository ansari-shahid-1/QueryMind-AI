from backend.database.query_service import execute_query


query = """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM analytics.orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""

result = execute_query(query)

print("Columns:", result["columns"])
print("Total rows:", result["row_count"])

for row in result["rows"]:
    print(row)