"""Build a local SQLite database from the GME 2024 Excel workbook.

Run from any working directory:
    python sql/02_build_sqlite_database.py

Place the source file at data/Anno 2024_12.xlsx first.
The source data and generated database should not be committed to Git.
"""

from pathlib import Path
import sqlite3

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "Anno 2024_12.xlsx"
DATABASE = ROOT / "data" / "electricity_prices_2024.db"


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(
            f"Source workbook not found: {SOURCE}\n"
            "Download the 2024 MGP historical data from GME and place it in data/."
        )

    raw = pd.read_excel(SOURCE, sheet_name="Prezzi-Prices")
    prices = raw.iloc[:, :3].copy()
    prices.columns = ["date", "hour", "price"]
    prices["date"] = pd.to_datetime(
        prices["date"].astype(str), format="%Y%m%d", errors="raise"
    )
    prices["hour"] = pd.to_numeric(prices["hour"], errors="raise").astype(int)
    prices["price"] = pd.to_numeric(prices["price"], errors="raise")

    if prices.isna().any().any():
        raise ValueError("Missing values detected in date, hour or price")
    if prices.duplicated(["date", "hour"]).any():
        raise ValueError("Duplicate (date, hour) combinations detected")
    if len(prices) != 8784 or prices["date"].nunique() != 366:
        raise ValueError("Unexpected 2024 dataset size or calendar coverage")

    day_counts = prices.groupby("date").size().value_counts().to_dict()
    if day_counts != {24: 364, 23: 1, 25: 1}:
        raise ValueError(f"Unexpected observations per day: {day_counts}")

    # Python convention: Monday=0, Sunday=6.
    prices["day_of_week"] = prices["date"].dt.dayofweek
    prices["date"] = prices["date"].dt.strftime("%Y-%m-%d")
    prices = prices.sort_values(["date", "hour"]).reset_index(drop=True)

    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE) as connection:
        prices.to_sql("electricity_prices", connection, if_exists="replace", index=False)
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_prices_date_hour "
            "ON electricity_prices (date, hour)"
        )
        count = connection.execute(
            "SELECT COUNT(*) FROM electricity_prices"
        ).fetchone()[0]

    print(f"Database created: {DATABASE}")
    print(f"Table: electricity_prices | rows: {count}")
    print("Columns: date, hour, price, day_of_week (Monday=0)")
    print(f"Observations per day: {day_counts}")


if __name__ == "__main__":
    main()
