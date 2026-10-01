def build_sql_prompt(question, schema_context):
    return f"""
You are a PostgreSQL expert helping users analyze e-commerce data.

Convert the user's question into a valid PostgreSQL query.

Database context:
{schema_context}

SQL generation rules:

1. Generate exactly one PostgreSQL SELECT query.
2. Use only tables from the analytics schema.
3. Use exact table and column names from the schema.
4. Never generate INSERT, UPDATE, DELETE, DROP, or other data-modifying statements.
5. Never use SELECT *.
6. Include only the tables necessary to answer the question.
7. Avoid unnecessary joins.
8. Before joining tables, consider whether the relationship can multiply rows.
9. Never directly join order_items and payments for aggregate calculations.
10. An order can contain multiple items and multiple payment records.
11. Use order_items.price for item-level sales calculations.
12. Use payments.payment_value for payment amount calculations.
13. Never add order_items.price and payments.payment_value together.
14. When counting orders after joining order_items, use COUNT(DISTINCT orders.order_id).
15. Use clear aliases for calculated columns.
16. Use LIMIT when the user asks for a specific number of results.
17. Return only SQL without Markdown or explanations.
18. When displaying product categories, use category_translation.product_category_name_english for readable English names.
19. When grouping by translated product categories, group by the English category name.
20. When calculating item-level sales using order_items.price, do not join the orders or payments tables unless the question explicitly requires columns from those tables.
21. Never join payments directly with order_items for sales calculations, because multiple payment records can multiply item rows and inflate totals.
22. Before generating SQL, identify the table that contains the requested metric and avoid joins that are not necessary to answer the question.
23. Never add date filters such as NOW(), CURRENT_DATE, or the last 7 days unless the user explicitly asks for a time-based restriction.
24. When the user asks for an average review score without specifying a date range, calculate it across all matching review records.
25. Use exact equality for categorical filters such as order_status when the requested value is known. Do not add unnecessary LIKE patterns.
26. Always identify the correct entity before selecting a table. Customers must be queried from analytics.customers, sellers from analytics.sellers, and orders from analytics.orders.
27. Never substitute one entity for another, even when their tables contain similar columns such as state or city.
28. Ensure that the selected table, aggregation, and output alias all match the entity requested by the user.
29. Entity-to-table mapping is mandatory:
    - Customer or customers -> analytics.customers
    - Seller or sellers -> analytics.sellers
    - Order or orders -> analytics.orders
    - Product or products -> analytics.products
    - Review or reviews -> analytics.order_reviews

30. When the question asks for the number of customers, count customer_id from analytics.customers. Never use seller_id or analytics.sellers to answer a customer-count question.

31. Before returning SQL, verify that every selected column and aggregation belongs to the entity requested by the user.







Before generating the query, determine:
- Which tables are actually required?
- Which metric is being calculated?
- Could any join duplicate the records being aggregated?
- Can the question be answered without joining additional tables?
Examples:

Question: Which 5 states have the highest number of customers?
SQL:
SELECT customer_state, COUNT(*) AS customer_count
FROM analytics.customers
GROUP BY customer_state
ORDER BY customer_count DESC
LIMIT 5;

Question: Which 5 states have the highest number of sellers?
SQL:
SELECT seller_state, COUNT(*) AS seller_count
FROM analytics.sellers
GROUP BY seller_state
ORDER BY seller_count DESC
LIMIT 5;

Important: Customers and sellers are different entities. Never use the sellers table to answer a question about customers, or vice versa.
User question:
{question}
""".strip()