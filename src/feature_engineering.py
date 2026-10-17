"""Leakage-aware calendar-aligned features for Italian MGP day-ahead prices.

For a forecast issued at 12:00 on D-1, only observed prices from D-2
or earlier are used. Input must contain columns date, hour, price.
"""

import pandas as pd

FEATURE_COLUMNS = [
    "hour", "day_of_week", "month", "price_2days_ago",
    "price_3days_ago", "price_last_week", "price_7day_mean",
    "price_7day_std",
]
HISTORICAL_FEATURE_COLUMNS = [
    "price_2days_ago", "price_3days_ago", "price_last_week",
    "price_7day_mean", "price_7day_std",
]


def build_dayahead_features(prices: pd.DataFrame, drop_incomplete: bool = True) -> pd.DataFrame:
    """Build the eight historical/calendar features from notebook 04.

    Historical prices are matched by calendar date and GME market hour,
    not by positional shifts, to accommodate 23/25-hour DST days.
    The seven-day standard deviation uses pandas' sample std (ddof=1).

    Args:
        prices: DataFrame with date, hour, price, one row per date/hour.
        drop_incomplete: If True, exclude rows missing required historical
            features, matching the notebook's modeling dataset.

    Returns:
        DataFrame sorted by date/hour containing date, hour, price,
        historical features and calendar features.
    """
    required = ["date", "hour", "price"]
    missing = set(required) - set(prices.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = prices[required].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["date", "hour"]).reset_index(drop=True)
    if df.duplicated(["date", "hour"]).any():
        raise ValueError("Duplicate date/hour pairs are not supported")

    result = df.copy()
    for lag in (2, 3, 7):
        historical = df.copy()
        historical["date"] = historical["date"] + pd.Timedelta(days=lag)
        historical = historical.rename(columns={"price": f"price_{lag}days_ago"})
        result = result.merge(
            historical[["date", "hour", f"price_{lag}days_ago"]],
            on=["date", "hour"], how="left", validate="one_to_one",
        )
    result = result.rename(columns={"price_7days_ago": "price_last_week"})
    result["day_of_week"] = result["date"].dt.dayofweek
    result["month"] = result["date"].dt.month

    historical_columns = []
    for lag in range(2, 9):
        name = f"historical_price_{lag}"
        historical = df.copy()
        historical["date"] = historical["date"] + pd.Timedelta(days=lag)
        historical = historical.rename(columns={"price": name})
        result = result.merge(
            historical[["date", "hour", name]],
            on=["date", "hour"], how="left", validate="one_to_one",
        )
        historical_columns.append(name)

    result["price_7day_mean"] = result[historical_columns].mean(axis=1, skipna=False)
    result["price_7day_std"] = result[historical_columns].std(axis=1, skipna=False)
    result = result.drop(columns=historical_columns)
    if drop_incomplete:
        result = result.dropna(subset=HISTORICAL_FEATURE_COLUMNS).copy()
    return result
