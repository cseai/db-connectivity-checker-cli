"""Microsoft SQL Server connectivity via pyodbc."""

import pyodbc

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Adjust if your system uses another ODBC driver name (see `odbcinst -q -d`).
_DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"


def connect():
    port = int(DB_PORT) if DB_PORT else 1433
    driver = _DEFAULT_DRIVER
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={DB_HOST},{port};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "LoginTimeout=5;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, timeout=5)


def test_query(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1")
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
