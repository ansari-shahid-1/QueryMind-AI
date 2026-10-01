import psycopg

from backend.database.connection import get_connection
from backend.database.query_service import execute_query


def test_row_limit():
    query = """
        SELECT customer_id
        FROM analytics.customers
    """

    try:
        execute_query(query)
        print("Row limit test: FAILED — oversized result was accepted.")

    except ValueError as error:
        if "more than 1000 rows" in str(error):
            print("Row limit test: PASSED — oversized result was rejected.")
        else:
            raise


def test_statement_timeout():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SET LOCAL statement_timeout = '10000ms'"
                )
                cur.execute("SELECT pg_sleep(11)")

        print("Timeout test: FAILED — query was not canceled.")

    except psycopg.errors.QueryCanceled:
        print("Timeout test: PASSED — query was canceled.")


if __name__ == "__main__":
    test_row_limit()
    test_statement_timeout()