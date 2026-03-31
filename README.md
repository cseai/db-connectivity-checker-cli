# Database connection checker

Small CLI to verify you can reach a remote **PostgreSQL**, **MySQL**, or **SQL Server** database before wiring it into Odoo or other apps.

## What you need

- **Python 3.10+** ([python.org](https://www.python.org/downloads/) or your OS package manager)
- Network access to the database host and port

## Setup (about one minute)

1. **Put the project folder** on this machine (clone, copy, or unzip).

2. **Open a terminal** in that folder (the directory that contains `main.py`).

3. **Create a virtual environment and install dependencies:**

   **Linux / macOS**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   **Windows (Command Prompt)**

   ```bat
   py -3 -m venv .venv
   .venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

   **Windows (PowerShell)**

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Configure the database** — copy the example env file and edit it with your real host, user, password, and database name:

   ```bash
   cp .env.example .env
   ```

   Open `.env` in any text editor and set at least `DB_HOST`, `DB_USER`, `DB_NAME`, and usually `DB_PASSWORD`. See the comments inside `.env.example` for what each variable does.

5. **Run a test** (pick the type you use):

   ```bash
   python main.py --db_type=postgres
   python main.py --db_type=mysql
   python main.py --db_type=mssql
   ```

   Success looks like: `[SUCCESS] Connected successfully` and `[RESULT] 1`.

## Tips

- Run **`python main.py --help`** to see options.
- Set **`DEBUG=true`** in `.env` if you need the full error traceback.
- **SQL Server only:** you need an [ODBC driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) installed on this PC. If connection fails with a driver error, check `db/mssql.py` and match `_DEFAULT_DRIVER` to a driver name listed by `odbcinst -q -d` (Linux/macOS) or ODBC Data Source Administrator (Windows).

Keep `.env` private; do not commit it to git.
