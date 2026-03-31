"""PostgreSQL connectivity via psycopg2."""

import psycopg2

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def connect():
    port = int(DB_PORT) if DB_PORT else 5432
    return psycopg2.connect(
        host=DB_HOST,
        port=port,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        connect_timeout=5,
    )


def test_query(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        row = cur.fetchone()
    return row[0] if row else None
