# Italian Electricity Price Forecasting

### Day-Ahead Electricity Price Prediction Using Python, SQL and Machine Learning

## Project Overview

This project develops and evaluates forecasting models for hourly electricity prices in the Italian day-ahead electricity market (MGP), using 2024 price data.

**Operational scenario:** at **12:00 on day D−1**, forecast the hourly prices for day D. The historical-price features are deliberately restricted to observations from **D−2 or earlier**, so the model does not rely on the complete set of D−1 prices that would not yet be available at issuance time.

The repository documents exploratory data analysis, SQL workflows, historical baselines, model development, and a chronological evaluation, emphasizing reproducibility, realistic feature availability, and transparent reporting.

## Technologies

- **Python:** pandas, NumPy, scikit-learn, Matplotlib
- **SQL / SQLite:** exploratory queries, database creation, and query validation
- **Jupyter Notebook:** reproducible analysis and model comparisons
- **GitHub:** version control and project documentation

## Dataset and Methodology

The source dataset contains **8,784 market-hour price observations from 2024**, covering 366 calendar days, including the daylight-saving transitions (one 23-hour day and one 25-hour day). Prices are expressed in **EUR/MWh**.

The source workbook is not redistributed in this repository. See [`data/README.md`](data/README.md) for data-source and setup notes.

Features include market hour, day of week, month, same-hour prices from D−2, D−3 and D−7, and the mean and standard deviation of seven historical same-hour prices (D−2 through D−8). Historical observations are joined by **calendar date and market hour** rather than positional row shifts, to handle daylight-saving changes appropriately. After requiring complete historical feature windows, **8,584 observations** remain.

The chronological split is:

| Period | Purpose | Observations |
|---|---|---:|
| January–June 2024 | Initial training | 4,168 |
| July–September 2024 | Validation and model comparison | 2,208 |
| October–December 2024 | Final evaluation period | 2,208 |

The historical **D−2 same-hour price** is used as the main operational baseline. Linear Regression and Random Forest are compared on the same leakage-aware feature set. The selected configurations are refitted using **January–September** observations before evaluation on October–December.

## Model Selection: Validation Results

Model selection is based on **July–September 2024 validation results**, not on which model happens to perform best on the final evaluation period.

| Model | MAE (EUR/MWh) | RMSE (EUR/MWh) |
|---|---:|---:|
| **Linear Regression** | **10.664** | **15.834** |
| Random Forest (full safe feature set) | 11.762 | 18.151 |
| D−2 historical baseline | 12.678 | 19.056 |

**Linear Regression is the validation-selected model.** Random Forest is retained as an important comparison model.

## Final Evaluation: October–December 2024

| Model | MAE (EUR/MWh) | RMSE (EUR/MWh) | MAE improvement vs D−2 |
|---|---:|---:|---:|
| **Linear Regression (validation-selected)** | 13.295 | 18.643 | 20.19% |
| Random Forest (comparison) | **13.052** | **18.218** | **21.65%** |
| D−2 historical baseline | 16.657 | 23.591 | — |

Both machine-learning models outperform the D−2 baseline in overall test MAE and RMSE. Although Random Forest achieves a slightly lower test MAE (by **0.243 EUR/MWh**), this does **not** retroactively change the validation-based selection of Linear Regression.

**Evaluation transparency:** the October–December test results had already been examined during earlier project experiments. This repository reports that limitation explicitly rather than presenting the test period as never previously inspected. The reconstructed model comparison uses consistent leakage-aware features, and test results are not used here to retune the models.

## Key Findings

- The operational 12:00 issuance time makes **feature availability and leakage prevention** central to the forecasting design.
- **Linear Regression performs best on validation**, while **Random Forest performs slightly better on the final test period**. Model rankings are therefore period-dependent in this analysis.
- Both models improve substantially over the D−2 historical baseline.
- The seven-day historical price mean and previous-week same-hour price are influential signals for both models; feature importance is examined using model-specific diagnostics and validation permutation importance.
- Error rates vary by hour and month. **December 2024 is considerably more difficult to forecast than November** in the test period.
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
│   └── 04_final_model_evaluation.ipynb
├── sql/        # SQLite database builder, exploratory queries, query tests
├── src/        # Reusable Python code
├── figures/    # Charts and diagnostic visualizations
└── reports/    # Technical reports and documentation
```

## Reproducibility

1. Obtain the original 2024 GME workbook and place it at `data/Anno 2024_12.xlsx` (see `data/README.md`).
2. Install the Python packages used by the notebooks: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, and `openpyxl`.
3. Open Jupyter from the repository and execute notebooks **01 → 04** in order. Each forecasting notebook reads the original workbook using the relative path `../data/Anno 2024_12.xlsx` when run from the `notebooks/` directory.
4. For the SQL workflow, follow [`sql/README.md`](sql/README.md).

The generated SQLite database and original Excel workbook are not intended to be committed to the repository.

## Project Roadmap

**Milestones 1–5 — Completed:** data validation and exploratory analysis; SQL workflow; historical forecasting baselines; model development and validation-based selection; final evaluation and hourly/monthly diagnostics.

**Further analysis:** investigate the differences between validation and test performance, including temporal market conditions and error distribution, without using the test period to retroactively optimize the reported models.

**Milestone 6 — External Data Integration (Planned):** investigate electricity demand forecasts, renewable generation forecasts, weather forecasts, and additional calendar or market variables. Each external input must be demonstrably **available by 12:00 on D−1** for the day-D prediction to avoid look-ahead leakage.
