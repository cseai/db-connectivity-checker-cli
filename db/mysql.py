"""MySQL connectivity via pymysql."""

import pymysql

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def connect():
    port = int(DB_PORT) if DB_PORT else 3306
    return pymysql.connect(
        host=DB_HOST,
        port=port,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
    )


def test_query(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        row = cur.fetchone()
    return row[0] if row else None
