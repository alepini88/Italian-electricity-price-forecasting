# SQL Analysis — Italian Electricity Prices

This directory contains the SQL component of the Italian Electricity Price Forecasting project.

The analysis uses SQLite to explore historical hourly electricity prices from the Italian Day-Ahead Market (MGP) in 2024.

## Files

| File | Description |
|---|---|
| `01_sql_exploratory_queries.sql` | 13 exploratory SQL queries covering descriptive statistics, hourly patterns, window functions, and price changes. |
| `02_build_sqlite_database.py` | Builds a local SQLite database from the original GME Excel dataset. |
| `03_test_sql_queries.py` | Executes all 13 SQL queries and reports whether they run successfully. |

## Data Source

**Provider:** Gestore dei Mercati Energetici (GME)

**Official historical data:** https://gme.mercatoelettrico.org/Home/Esiti/Elettricita/MGP/Statistiche/DatiStorici

The original dataset is not redistributed in this repository. Users should consult the official source and its usage conditions.

## Requirements

- Python 3
- pandas
- openpyxl
- SQLite (available through Python's standard `sqlite3` module)

Install the required Python packages:

```bash
python -m pip install pandas openpyxl
```

## How to Run

Run the following commands from the repository's root directory.

**1. Obtain the dataset**

Place the original Excel file in:

```text
data/Anno 2024_12.xlsx
```

The database-building script expects the `Prezzi-Prices` worksheet.

**2. Build the SQLite database**

```bash
python sql/02_build_sqlite_database.py
```

This creates:

```text
data/electricity_prices_2024.db
```

The database contains a table named `electricity_prices` with the following columns:

| Column | Description |
|---|---|
| `date` | Trading date |
| `hour` | Market hour |
| `price` | Electricity price (EUR/MWh) |
| `day_of_week` | Day of the week, Monday = 0 |

**3. Validate the SQL queries**

```bash
python sql/03_test_sql_queries.py
```

Expected result:

```text
SUCCESS: 13/13 queries executed.
```

The validation script checks that the queries execute successfully. It does not independently prove the analytical correctness of every query.

## Dataset Validation

The 2024 dataset contains:

- 8,784 hourly observations.
- 366 calendar days.
- 364 days with 24 observations.
- One day with 23 observations (March 31, 2024).
- One day with 25 observations (October 27, 2024).

The two irregular days correspond to daylight saving time transitions.

## Important Forecasting Consideration

The SQL queries are intended for exploratory analysis.

Row-based lag functions such as `LAG(24)` and `LAG(168)` do not always represent the same clock hour on previous calendar days, particularly around daylight saving time transitions.

Furthermore, exploratory lag calculations must not automatically be treated as valid forecasting features.

The project's final day-ahead forecasting model uses only information available at the prediction issuance time (12:00 on the preceding day), to avoid data leakage.

## Project Roadmap

The SQL analysis supports the subsequent forecasting stages, including historical baselines, Random Forest development, final model evaluation, and future integration of external ex-ante variables..
