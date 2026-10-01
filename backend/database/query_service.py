from backend.database.connection import get_connection
from backend.services.sql_validator import validate_query


MAX_RESULT_ROWS = 1000
STATEMENT_TIMEOUT_MS = 10000


def execute_query(query, params=None):
    is_valid, message = validate_query(query)

    if not is_valid:
        raise ValueError(message)

    query = query.strip().rstrip(";")

    limited_query = f"""
        SELECT *
        FROM ({query}) AS querymind_result
        LIMIT {MAX_RESULT_ROWS + 1}
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT_MS}ms'"
            )

            cur.execute(limited_query, params)

            columns = [column.name for column in cur.description]
            rows = cur.fetchall()

            if len(rows) > MAX_RESULT_ROWS:
                raise ValueError(
                    f"Query returned more than {MAX_RESULT_ROWS} rows. "
                    "Please refine your question."
                )

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }