# Italian Electricity Price Forecasting

### Day-Ahead Electricity Price Prediction Using Python and Machine Learning

## Project Overview

This project develops and evaluates machine learning models to forecast hourly electricity prices in the Italian electricity market.

The forecasting scenario assumes that predictions for the following day are issued at **12:00 on the previous day**. Feature engineering is therefore designed to use only information available at the forecast issuance time.

The project combines time-series analysis, data preparation, predictive modeling, and error diagnostics, with an emphasis on reproducibility and realistic forecasting conditions.

## Technologies

- **Python:** pandas, NumPy, scikit-learn, Matplotlib
- **SQL:** data extraction, preparation, and validation
- **Jupyter Notebook:** experimentation and analysis
- **GitHub:** version control and project documentation

## Dataset and Methodology

The initial dataset contains **8,784 hourly electricity price observations for 2024**, including the daylight saving time transitions.

The modeling workflow includes:

1. Data quality checks and time-series validation.
2. Development of historical-price forecasting baselines.
3. Linear Regression and Random Forest experiments.
4. Construction of leakage-aware day-ahead features.
5. Chronological training, validation, and test splits.
6. Evaluation using MAE, RMSE, and detailed error analysis.

The final Random Forest model uses calendar information and historical electricity price features, including lagged prices and rolling historical statistics.

## Final Model Performance

The final evaluation was performed on the **October–December 2024 test period**, held out from model development.

| Metric | Day-Ahead Baseline | Random Forest | Improvement |
|---|---:|---:|---:|
| MAE (EUR/MWh) | 16.657 | 13.052 | 21.65% |
| RMSE (EUR/MWh) | 23.591 | 18.218 | 22.78% |

The Random Forest outperformed the baseline across all 24 hourly groups in the test period.

## Key Findings

- Leakage-aware feature engineering is essential for realistic day-ahead forecasting.
- Random Forest improved overall predictive accuracy compared with the historical-price baseline.
- Forecast errors are larger during unusual electricity price events.
- The model tends to overestimate very low prices and underestimate high prices.
- Additional information beyond historical prices may help improve forecasting performance.

## Repository Structure

```text
data/       Dataset documentation
notebooks/  Exploratory analysis and model experiments
src/        Reusable Python code
sql/        SQL queries
figures/    Charts and diagnostic visualizations
reports/    Technical reports and documentation
```

## Project Roadmap

**Milestones 1–5 — Initial forecasting workflow and model evaluation**

Completed analyses include data validation, historical baselines, regression experiments, Random Forest modeling, leakage-aware feature engineering, and test-set error diagnostics.

**Milestone 6 — External Data Integration (Planned)**

The next development phase will investigate external variables relevant to the Italian electricity market, including:

- Electricity demand forecasts
- Renewable generation forecasts
- Weather forecasts
- Additional calendar and market information

# Data Sources

## Historical Electricity Prices — Italy, 2024

**Source:** Gestore dei Mercati Energetici S.p.A. (GME)

**Market:** Mercato del Giorno Prima (MGP)

**Period:** January 1 – December 31, 2024

**Frequency:** Hourly

**Observations:** 8,784

### Official Data Source

https://gme.mercatoelettrico.org/Home/Esiti/Elettricita/MGP/Statistiche/DatiStorici

The historical dataset was obtained from the official GME website.

### Data Availability and Usage

The original Excel dataset is not redistributed in this repository due to the applicable GME usage conditions.

Users should consult the official source and its terms of use before obtaining or processing the data.

For local execution, the EDA notebook expects the following file:

`data/Anno 2024_12.xlsx`

The file is read from the `Prezzi-Prices` worksheet.

### Data Quality

The dataset contains 8,784 hourly observations covering 366 days in 2024.

The analysis identified no missing values or duplicate date-hour combinations. The two daylight saving time transition dates contain 23 and 25 observations, respectively.

### Future Data Integration

Milestone 6 will investigate additional electricity market variables, including demand forecasts, renewable generation forecasts, and weather forecasts, subject to their availability and usage conditions.

Only data available at the forecast issuance time will be considered as predictive inputs.

## Current Status

The initial forecasting experiments are complete. The repository is being organized and documented, and the next technical phase will focus on integrating external data and evaluating improved forecasting models.
