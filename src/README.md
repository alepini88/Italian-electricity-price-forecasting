# Source Code

This directory contains reusable Python modules extracted from the project's Jupyter notebooks. The modules support data loading, leakage-aware feature engineering, and forecasting model evaluation.

## Modules

| File | Purpose |
|---|---|
| `data_loader.py` | Loads and prepares hourly Italian day-ahead electricity prices from the GME 2024 Excel workbook. |
| `feature_engineering.py` | Builds calendar features, historical price lags, and rolling historical statistics for day-ahead forecasting. |
| `evaluation.py` | Computes forecasting metrics, compares models, and summarizes prediction errors by hour and month. |

## Forecasting setup

The project simulates a forecast made at **12:00 on day D−1** for all market hours of day D.

To avoid target leakage, historical price features use only information from **D−2 or earlier**.

The eight model features are:

- `hour`
- `day_of_week`
- `month`
- `price_2days_ago`
- `price_3days_ago`
- `price_last_week`
- `price_7day_mean`
- `price_7day_std`

The seven-day historical statistics use observations from **D−2 through D−8**, matched by calendar date and GME market hour.

## Basic usage

Run the following example from a Jupyter notebook located in the project's `notebooks/` directory:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parent / "src"))

from data_loader import load_gme_prices
from feature_engineering import build_dayahead_features, FEATURE_COLUMNS
from evaluation import evaluation_metrics

from sklearn.linear_model import LinearRegression

prices = load_gme_prices()
features = build_dayahead_features(prices)

train_val = features[features["date"] < "2024-10-01"]
test = features[features["date"] >= "2024-10-01"]

model = LinearRegression()
model.fit(train_val[FEATURE_COLUMNS], train_val["price"])

predictions = model.predict(test[FEATURE_COLUMNS])

print(evaluation_metrics(test["price"], predictions))
```

The original GME Excel workbook must be available locally in the project's `data/` directory.

## Reproducibility checks

The modules were tested together using the 2024 GME dataset.

| Check | Verified result |
|---|---:|
| Original hourly observations | 8,784 |
| Complete feature observations | 8,584 |
| Training observations (Jan–Jun) | 4,168 |
| Validation observations (Jul–Sep) | 2,208 |
| Test observations (Oct–Dec) | 2,208 |
| Linear Regression test MAE | 13.295 €/MWh |
| Linear Regression test RMSE | 18.643 €/MWh |

The final Linear Regression model is refitted on January–September data and evaluated on October–December data. Model selection was based on validation performance.

## Related notebooks

- `01_exploratory_data_analysis.ipynb`
- `02_forecasting_baselines.ipynb`
- `03_model_development.ipynb`
- `04_final_model_evaluation.ipynb`
- `05_validation_vs_test_diagnostics.ipynb`

The notebooks provide the full analytical workflow, visualizations, model comparison, and interpretation of results.
   
