"""Load 2024 GME/MGP hourly electricity prices for the forecasting project.

The source Excel workbook is stored locally and is not distributed in GitHub.
"""

from pathlib import Path

import pandas as pd


DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "Anno 2024_12.xlsx"


def load_gme_prices(data_path=None):
    """Return a DataFrame with ``date``, ``hour``, and ``price`` columns.

    Parameters
    ----------
    data_path : str or pathlib.Path, optional
        Excel workbook location. By default, use the repository's data folder.

    Notes
    -----
    GME market hours are preserved as provided (including DST hour 25).
    No rows are removed, no historical features are created, and no prices
    are shifted. This mirrors the data-loading cell of notebook 01.
    """
    path = Path(data_path) if data_path is not None else DEFAULT_DATA_PATH
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path.resolve()}\n"
            "Place the source Excel file in the project's data/ directory."
        )

    source = pd.read_excel(path, sheet_name="Prezzi-Prices")
    prices = source.iloc[:, [0, 1, 2]].copy()
    prices.columns = ["date", "hour", "price"]
    prices["date"] = pd.to_datetime(
        prices["date"].astype(str), format="%Y%m%d"
    )
    return prices
