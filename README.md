# Italian Electricity Price Forecasting

### Day-Ahead Electricity Price Prediction Using Python, SQL and Machine Learning

## Project Overview

This project develops and evaluates forecasting models for hourly electricity prices in the Italian day-ahead electricity market (MGP), using 2024 price data.

**Operational scenario:** at **12:00 on day D−1**, forecast the hourly prices for day D. Historical-price features are restricted to observations from **D−2 or earlier**, avoiding reliance on the complete set of D−1 prices, which would not yet be available at issuance time.

The repository documents exploratory data analysis, SQL workflows, historical baselines, model development, chronological evaluation, and a follow-up analysis of market conditions in the validation and test periods. Emphasis is placed on reproducibility, realistic feature availability, and transparent reporting.

## Technologies

- **Python:** pandas, NumPy, scikit-learn, Matplotlib
- **SQL / SQLite:** exploratory queries, database creation, and query validation
- **Jupyter Notebook:** reproducible analysis and model comparisons
- **GitHub:** version control and project documentation

## Dataset and Methodology

The source dataset contains **8,784 market-hour price observations from 2024**, covering 366 calendar days, including daylight-saving transitions (one 23-hour day and one 25-hour day). Prices are expressed in **EUR/MWh**.

The source workbook is not redistributed in this repository. See [`data/README.md`](data/README.md) for data-source and setup notes.

Forecasting features include market hour, day of week, month, same-hour prices from D−2, D−3 and D−7, and the mean and standard deviation of seven historical same-hour prices (D−2 through D−8). Historical observations are joined by **calendar date and market hour** rather than positional row shifts to handle daylight-saving changes appropriately. After requiring complete historical feature windows, **8,584 observations** remain.

The chronological modeling split is:

| Period | Purpose | Observations |
|---|---|---:|
| January–June 2024 | Initial training | 4,168 |
| July–September 2024 | Validation and model comparison | 2,208 |
| October–December 2024 | Final evaluation period | 2,208 |

The historical **D−2 same-hour price** is the main operational baseline. Linear Regression and Random Forest are compared using the same leakage-aware feature set. The selected configurations are refitted on **January–September** observations before evaluation on October–December.

## Model Selection: Validation Results

Model selection is based on **July–September 2024 validation results**, not on which model happens to perform best on the final evaluation period.

| Model | MAE (EUR/MWh) | RMSE (EUR/MWh) |
|---|---:|---:|
| **Linear Regression** | **10.664** | **15.834** |
| Random Forest (full safe feature set) | 11.762 | 18.151 |
| D−2 historical baseline | 12.678 | 19.056 |

**Linear Regression is the validation-selected model.** Random Forest is retained as a comparison model.

## Final Evaluation: October–December 2024

| Model | MAE (EUR/MWh) | RMSE (EUR/MWh) | MAE improvement vs D−2 |
|---|---:|---:|---:|
| **Linear Regression (validation-selected)** | 13.295 | 18.643 | 20.19% |
| Random Forest (comparison) | **13.052** | **18.218** | **21.65%** |
| D−2 historical baseline | 16.657 | 23.591 | — |

Both machine-learning models outperform the D−2 baseline in overall test MAE and RMSE. Although Random Forest achieves a slightly lower test MAE (by **0.243 EUR/MWh**), this does **not** retroactively change the validation-based selection of Linear Regression.

**Evaluation transparency:** the October–December test results had already been examined during earlier project experiments. This limitation is reported explicitly rather than presenting the test period as never previously inspected. The reconstructed model comparison uses consistent leakage-aware features, and test results are not used here to retune the models.

## Validation vs Test Market Diagnostics

Notebook [`05_validation_vs_test_diagnostics.ipynb`](notebooks/05_validation_vs_test_diagnostics.ipynb) compares observed market conditions in **July–September (validation)** and **October–December (test)** to investigate whether differences in price behavior coincide with differences in forecast accuracy.

| Observed price statistic | Validation (Jul–Sep) | Test (Oct–Dec) |
|---|---:|---:|
| Source market-hour observations | 2,208 | 2,209 |
| Mean price (EUR/MWh) | 119.317 | 127.506 |
| Standard deviation of price levels (EUR/MWh) | 26.451 | 28.515 |
| Mean absolute same-hour day-to-day price change (EUR/MWh) | 10.726 | 12.381 |

The mean absolute same-hour day-to-day price change is approximately **15.4% higher** in the test period. **December** has the highest monthly price-level standard deviation (**35.098 EUR/MWh**) and mean absolute same-hour day-to-day change (**16.845 EUR/MWh**) among the six months analyzed. It also has the highest test-month forecasting errors: **19.659 EUR/MWh MAE** for Linear Regression and **19.019 EUR/MWh** for Random Forest.

The descriptive analysis uses **original observed prices**, not the filtered modeling dataset. The test period therefore contains **2,209 source market-hour observations**, including the additional hour at the October daylight-saving transition, compared with **2,208 modeling observations** in the test split.

These differences are **consistent with**, but do **not establish the cause of**, the higher forecast errors. Price-level dispersion and day-to-day movements are distinct descriptive measures. The latter also differs from the project's D−2-or-earlier forecasting information horizon. No model is reselected or retuned using these already-inspected test results.

## Key Findings

- The operational 12:00 issuance time makes **feature availability and leakage prevention** central to the forecasting design.
- **Linear Regression performs best on validation**, while **Random Forest performs slightly better on the final test period**; model rankings vary by period.
- Both models improve substantially over the D−2 historical baseline.
- The seven-day historical price mean and previous-week same-hour price are influential signals for both models; feature importance is examined using model-specific diagnostics and validation permutation importance.
- Forecast errors vary by hour and month. **December 2024 is considerably more difficult to forecast than November** in the test period.
- Observed test-period prices have higher average levels, slightly greater dispersion, and larger average same-hour day-to-day movements than validation-period prices. These findings are **descriptive, not causal**.
- Additional ex-ante information, particularly demand, renewable generation, and weather forecasts, is a promising direction for future investigation; its benefit has not yet been established in this project.

## Repository Structure

```text
.
├── README.md
├── data/       # Dataset documentation (original workbook not redistributed)
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_forecasting_baselines.ipynb
│   ├── 03_model_development.ipynb
│   ├── 04_final_model_evaluation.ipynb
│   └── 05_validation_vs_test_diagnostics.ipynb
├── sql/        # SQLite database builder, exploratory queries, query tests
├── src/        # Reusable Python code
├── figures/    # Charts and diagnostic visualizations
└── reports/    # Technical reports and documentation
```

## Reproducibility

1. Obtain the original 2024 GME workbook and place it at `data/Anno 2024_12.xlsx` (see `data/README.md`).
2. Install the Python packages used by the notebooks: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, and `openpyxl`.
3. Open Jupyter from the repository and execute notebooks **01 → 05** in order. Run them from the `notebooks/` directory; the notebooks read the workbook using the relative path `../data/Anno 2024_12.xlsx`.
4. For the SQL workflow, follow [`sql/README.md`](sql/README.md).

The generated SQLite database and original Excel workbook are not intended to be committed to the repository. Notebook 05 presents previously observed model MAE values for context; it does not independently recompute model predictions.

## Project Roadmap

**Milestones 1–5 — Completed:** data validation and exploratory analysis; SQL workflow; historical forecasting baselines; model development and validation-based selection; final evaluation and hourly/monthly error diagnostics.

**Additional diagnostic analysis — Completed:** comparison of observed validation and test market conditions, including price distributions, monthly dispersion, and same-hour day-to-day price movements (Notebook 05). This is a descriptive analysis and does not use the test period to retroactively optimize the reported models.

**Milestone 6 — External Data Integration (Planned):** investigate electricity demand forecasts, renewable generation forecasts, weather forecasts, and additional calendar or market variables. Each external input must be demonstrably **available by 12:00 on D−1** for the day-D prediction to avoid look-ahead leakage. Future model comparisons would benefit from additional forward periods or rolling-origin evaluation with predefined selection rules.
