"""Microsoft SQL Server connectivity via pyodbc."""

import pyodbc

from config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DEBUG,
    MSSQL_ENCRYPT,
    MSSQL_ODBC_DRIVER,
)

# Used only when MSSQL_ODBC_DRIVER is not set in .env. Prefer setting MSSQL_ODBC_DRIVER
# to match `odbcinst -q -d` on this machine (names differ: 17 vs 18, FreeTDS, etc.).
_FALLBACK_DRIVER = "ODBC Driver 17 for SQL Server"


def connect():
    port = int(DB_PORT) if DB_PORT else 1433
    driver = MSSQL_ODBC_DRIVER or _FALLBACK_DRIVER
    # Driver 18 defaults to strict TLS; older SQL Server / OpenSSL stacks may need
    # Encrypt=optional or Encrypt=no (lab only). See MSSQL_ENCRYPT in .env.
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={DB_HOST},{port};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"Encrypt={MSSQL_ENCRYPT};"
        "TrustServerCertificate=yes;"
        "LoginTimeout=5;"
    )
    if DEBUG:
        import logger

        safe = conn_str.replace(DB_PASSWORD, "***") if DB_PASSWORD else conn_str
        logger.info(
            f"ODBC MSSQL_ENCRYPT effective value: {MSSQL_ENCRYPT!r} "
            "(shell env can override .env; run `unset MSSQL_ENCRYPT` if wrong)"
        )
        logger.info(f"ODBC connection string (sanitized): {safe}")
    return pyodbc.connect(conn_str, timeout=5)


def test_query(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1")
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
