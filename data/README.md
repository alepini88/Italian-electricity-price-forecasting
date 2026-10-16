
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
