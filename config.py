"""Load configuration from environment (.env via python-dotenv)."""

import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "").lower() in ("true", "1", "yes")

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")

# MSSQL only: exact ODBC driver name as shown by `odbcinst -q -d` (optional).
MSSQL_ODBC_DRIVER = (os.getenv("MSSQL_ODBC_DRIVER") or "").strip()

# MSSQL only: ODBC Encrypt= value (optional, no, yes, mandatory, strict). Default optional.
MSSQL_ENCRYPT = (os.getenv("MSSQL_ENCRYPT") or "optional").strip()
