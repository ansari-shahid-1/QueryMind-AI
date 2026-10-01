from backend.database.connection import get_connection


def test_connection():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_database(),
                    current_user,
                    COUNT(*)
                FROM analytics.customers;
            """)

            result = cur.fetchone()

            print("Database:", result[0])
            print("User:", result[1])
            print("Total customers:", result[2])


if __name__ == "__main__":
    test_connection()