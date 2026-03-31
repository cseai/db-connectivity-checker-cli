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

### SQL Server (`--db_type=mssql`)

`pyodbc` needs two things on the machine, not just `pip`:

1. **ODBC driver manager** (provides `libodbc.so.2` and the **`odbcinst`** tool on Linux). If you see `ImportError: libodbc.so.2` or **`odbcinst: command not found`**, install it first, for example:
   - **Debian / Ubuntu:** `sudo apt install unixodbc` (this installs `odbcinst`; you can also use `sudo apt install odbcinst` if your distro suggests it)
   - **Fedora / RHEL:** `sudo dnf install unixODBC`
2. **[Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos-linux)** for your OS (Linux, macOS, or Windows).

**Ubuntu (including 24.04):** Minimal servers often have **no `curl`**. If you run Microsoft’s install commands without it, the signing key/repo steps fail (`gpg: no valid OpenPGP data found`), nothing is added to APT, and **`msodbcsql18` cannot be located**. Install `curl` first, then use Microsoft’s **`packages-microsoft-prod.deb`** method (not a broken hand-made `.list` file):

```bash
sudo apt install -y curl ca-certificates
cd /tmp
curl -fsSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm -f packages-microsoft-prod.deb
sudo apt update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

If you prefer **`wget`**: `wget https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb` then `sudo dpkg -i packages-microsoft-prod.deb` and continue with `apt update` / `apt install` as above. Remove any empty or broken `mssql-release.list` under `/etc/apt/sources.list.d/` from earlier failed attempts, and delete a zero-byte `/usr/share/keyrings/microsoft-prod.gpg` before retrying.

**Remote SQL Server version:** If the *server* runs **SQL Server 2017** (internal version **14.x** in `SELECT @@VERSION`), you still use **ODBC Driver 17 or 18 for SQL Server** on *this* machine. There is no separate “v14 ODBC driver”—client driver name and server major version are unrelated. ODBC Driver 17+ supports SQL Server 2017 and newer.

After step 1–2, list drivers with `odbcinst -q -d` (Linux/macOS) or ODBC Data Source Administrator (Windows). If `odbcinst` is still missing, the `unixodbc` package is not installed yet. Put the exact name in `.env` as **`MSSQL_ODBC_DRIVER`** (for example `ODBC Driver 17 for SQL Server`). If you see **Can't open lib … file not found**, the driver is missing or the name does not match what is installed—fix the install or adjust `MSSQL_ODBC_DRIVER`.

If you see **`SSL Provider` / `unsupported protocol`**, the ODBC driver and server disagree on TLS (common with **ODBC Driver 18** on Ubuntu and older SQL Server). The tool defaults to **`Encrypt=optional`** via **`MSSQL_ENCRYPT`**; if needed for a private test network only, try **`MSSQL_ENCRYPT=no`**, or enable **TLS 1.2** on SQL Server.

#### If `odbcinst` says `SQLGetPrivateProfileString failed`

unixODBC is installed, but it cannot read the driver config (wrong paths, bad permissions, or broken `.ini` files). Try in order:

1. **Clear bad environment overrides** (common on shared or custom setups). In the same shell you use for `odbcinst`:
   ```bash
   unset ODBCSYSINI ODBCINI ODBCINSTINI
   odbcinst -q -d
   ```
2. **See where unixODBC looks:** `odbcinst -j` — check that the paths it prints exist and that you can read the files (e.g. `ls -la /etc/odbcinst.ini`).
3. **Try as root:** `sudo odbcinst -q -d`. If that works but your user fails, fix permissions on `/etc/odbcinst.ini` / `/etc/odbc.ini` or stop pointing `ODBC*` variables at directories that are wrong.
4. **Repair the stack:** `sudo apt install --reinstall unixodbc` (Debian/Ubuntu), then install the [Microsoft ODBC driver](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos-linux) again if needed.
5. **If both your user *and* `sudo` get `SQLGetPrivateProfileString failed`**, the driver catalog file is usually missing or broken. A **0-byte** `/etc/odbcinst.ini` (shown by `ls -l` as size `0`) causes this—restore a minimal file as below. Inspect and reset it:
   ```bash
   odbcinst -j
   ls -la /etc/odbcinst.ini
   sudo head -5 /etc/odbcinst.ini
   ```
   Back up and install a **minimal valid** catalog (empty driver list; you reinstall the Microsoft driver afterward to register drivers again):
   ```bash
   sudo cp -a /etc/odbcinst.ini /etc/odbcinst.ini.bak 2>/dev/null || true
   printf '[ODBC Drivers]\n' | sudo tee /etc/odbcinst.ini
   odbcinst -q -d
   ```
   If that prints no error (output may be empty), reinstall the Microsoft ODBC driver so `odbcinst -q -d` lists **ODBC Driver 17/18 for SQL Server** again.

Keep `.env` private; do not commit it to git.
