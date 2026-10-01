import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user;")
            database, user = cur.fetchone()

            print("Database connection successful!")
            print(f"Database: {database}")
            print(f"User: {user}")

except Exception as error:
    print("Database connection failed.")
    print(error)