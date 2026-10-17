"""Reusable forecast evaluation utilities for Italian MGP hourly prices.

Extracted from the methodology in notebook 04. Inputs must contain observed
prices and prediction columns; this module does not fit or select models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluation_metrics(actual, prediction):
    """Return MAE and RMSE in the same units as the observed prices."""
    return {
        "MAE": mean_absolute_error(actual, prediction),
        "RMSE": np.sqrt(mean_squared_error(actual, prediction)),
    }


def compare_models(predictions, model_columns, actual_column="price"):
    """Compare model predictions with observations; one row per model."""
    return pd.DataFrame([
        {"Model": name, **evaluation_metrics(predictions[actual_column], predictions[name])}
        for name in model_columns
    ])


def hourly_mae(predictions, model_columns, actual_column="price", hour_column="hour"):
    """Mean absolute error for each GME market hour (1–24, possibly 25)."""
    errors = predictions[[hour_column]].copy()
    for name in model_columns:
        errors[name] = (predictions[actual_column] - predictions[name]).abs()
    return errors.groupby(hour_column)[list(model_columns)].mean()


def monthly_diagnostics(predictions, model_columns, actual_column="price", date_column="date"):
    """Monthly MAE and mean signed error (prediction minus actual)."""
    diagnostics = predictions.copy()
    diagnostics["month"] = pd.to_datetime(diagnostics[date_column]).dt.strftime("%Y-%m")
    rows = []
    for month, group in diagnostics.groupby("month", sort=True):
        for name in model_columns:
            rows.append({
                "Month": month,
                "Model": name,
                "MAE": mean_absolute_error(group[actual_column], group[name]),
                "Mean error (pred - actual)": (group[name] - group[actual_column]).mean(),
            })
    return pd.DataFrame(rows)
