"""CLI: test remote database connectivity (PostgreSQL, MySQL, MSSQL)."""

import argparse
import importlib
import sys
import traceback

import config
import logger

DB_LABELS = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mssql": "MSSQL",
}

DB_MODULE_PATH = {
    "postgres": "db.postgres",
    "mysql": "db.mysql",
    "mssql": "db.mssql",
}


def _friendly_error(exc: BaseException) -> str:
    msg = str(exc).strip()
    low = msg.lower()

    if "timeout" in low or "timed out" in low:
        return "Connection timed out (check host, port, and firewall)."
    if "refused" in low or "actively refused" in low:
        return "Connection refused (server not listening or wrong port)."
    if (
        "authentication failed" in low
        or "password authentication" in low
        or "access denied" in low
        or "login failed" in low
        or "18456" in msg
        or "1045" in msg
    ):
        return "Authentication failed (check user and password)."
    if "could not translate host" in low or "name or service not known" in low:
        return "Host could not be resolved (check DB_HOST)."
    if "ssl" in low and "certificate" in low:
        return f"SSL/certificate error: {msg[:200]}"

    return msg[:500] if len(msg) > 500 else msg


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test connectivity to a remote SQL database."
    )
    parser.add_argument(
        "--db_type",
        required=True,
        choices=["postgres", "mysql", "mssql"],
        help="Database type: postgres, mysql, or mssql",
    )
    args = parser.parse_args()

    for name, val in (
        ("DB_HOST", config.DB_HOST),
        ("DB_USER", config.DB_USER),
        ("DB_NAME", config.DB_NAME),
    ):
        if not (val or "").strip():
            logger.error(f"{name} is missing or empty (set it in .env).")
            return 1

    label = DB_LABELS[args.db_type]
    mod = importlib.import_module(DB_MODULE_PATH[args.db_type])

    logger.info(f"Trying {label}...")
    conn = None
    try:
        conn = mod.connect()
        logger.success("Connected successfully")
        logger.info("Running test query...")
        value = mod.test_query(conn)
        logger.result(str(value))
    except Exception as exc:
        logger.error(_friendly_error(exc))
        if config.DEBUG:
            traceback.print_exc()
        return 1
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
