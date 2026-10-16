"""Run the project's exploratory SQL queries against a local SQLite database.

From the repository root:
    python sql/03_test_sql_queries.py

The GME dataset and generated database remain local; neither is redistributed.
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SQL_FILE = ROOT / "sql" / "01_sql_exploratory_queries.sql"
DATABASE = ROOT / "data" / "electricity_prices_2024.db"
EXPECTED_QUERIES = 13


def load_queries(path: Path) -> list[str]:
    """Parse complete SQL statements, ignoring full-line SQL comments."""
    text = path.read_text(encoding="utf-8-sig")
    statements = []
    pending = ""
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("--"):
            continue
        pending += line
        if sqlite3.complete_statement(pending):
            statement = pending.strip()
            if statement:
                statements.append(statement)
            pending = ""
    if pending.strip():
        raise ValueError("Incomplete SQL statement at the end of the file.")
    return statements


def main() -> int:
    if not SQL_FILE.is_file():
        print(f"ERROR: SQL file not found: {SQL_FILE}")
        return 1
    if not DATABASE.is_file():
        print(f"ERROR: SQLite database not found: {DATABASE}")
        print("First run: python sql/02_build_sqlite_database.py")
        return 1

    try:
        queries = load_queries(SQL_FILE)
        if len(queries) != EXPECTED_QUERIES:
            raise ValueError(
                f"Expected {EXPECTED_QUERIES} queries, found {len(queries)}."
            )

        # Read-only connection prevents accidental modifications to local data.
        with sqlite3.connect(f"{DATABASE.as_uri()}?mode=ro", uri=True) as connection:
            for number, query in enumerate(queries, start=1):
                if not query.lstrip().upper().startswith(("SELECT", "WITH")):
                    raise ValueError(f"Query {number} is not a read-only SELECT/CTE.")
                try:
                    cursor = connection.execute(query)
                    first_row = cursor.fetchone()
                except sqlite3.Error as exc:
                    raise RuntimeError(f"Query {number} failed: {exc}") from exc
                print(f"Query {number:02d}: OK | First row: {first_row}")

        print(f"\nSUCCESS: {len(queries)}/{EXPECTED_QUERIES} queries executed.")
        return 0
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
