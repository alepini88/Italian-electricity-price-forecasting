-- Italian Electricity Price Forecasting | SQL Exploratory Analysis
-- Source: SQL queries 1–13 from the original SQL and ML notebook.
-- Dialect: SQLite
-- Expected table: electricity_prices(date, hour, price, day_of_week).
-- day_of_week must be populated during data preparation; it is not part of the three-column raw Excel extraction.
-- NOTE: row-based LAG offsets (24, 168) are observational lags, not always same-clock-hour lags across DST.
-- NOTE: these queries are descriptive; row-based lag features are NOT approved for the 12:00 day-ahead model.
-- Run after creating/populating the electricity_prices table.

-- Query 1
SELECT AVG(price) AS average_price
FROM electricity_prices;

-- Query 2
SELECT COUNT(*) AS total_rows, AVG(price) AS average_price,
MIN(price) AS minimum_price, MAX(price) AS maximum_price FROM electricity_prices;

-- Query 3
SELECT day_of_week, AVG(price) AS average_price FROM electricity_prices 
GROUP BY day_of_week ORDER BY day_of_week;

-- Query 4
SELECT hour, AVG(price) AS average_price FROM electricity_prices 
GROUP BY hour ORDER BY hour;

-- Query 5
SELECT 
      COUNT(*) AS high_price_hours,
      AVG(price) AS average_high_price
FROM electricity_prices 
WHERE price > 150;

-- Query 6
SELECT hour,
COUNT(*) AS high_price_hours
FROM electricity_prices
WHERE price > 150
GROUP BY hour
ORDER BY hour;

-- Query 7
SELECT hour,
COUNT(*) AS total_observations,
SUM(CASE WHEN price > 150 THEN 1 ELSE 0 END)
   AS high_price_count,
ROUND(100.0 * SUM(CASE WHEN price >150 THEN 1 ELSE 0 END)/COUNT(*),2)
AS high_price_pct
FROM electricity_prices
GROUP BY hour
ORDER BY high_price_pct DESC;

-- Query 8
SELECT day_of_week, ROUND(AVG(price),2) AS average_price
FROM electricity_prices
GROUP BY day_of_week
HAVING AVG(price) > 110
ORDER BY AVG(price) DESC;

-- Query 9
SELECT date,
       hour,
       price,
       LAG(price,1) OVER (ORDER BY date, hour) AS previous_price,
       price - LAG(price,1) OVER (ORDER BY date,hour) AS price_change
FROM electricity_prices
ORDER BY date, hour
LIMIT 10;

-- Query 10
SELECT date,
       hour,
       price,
       LAG(price,1) OVER (ORDER BY date, hour) AS lag_1,
       LAG(price, 24) OVER (ORDER BY date, hour) AS lag_24,
       LAG(price, 168) OVER (ORDER BY date, hour) AS lag_168
FROM electricity_prices
ORDER BY date, hour
LIMIT 200;

-- Query 11
SELECT date,
       hour,
       price,
       LAG(price,1) OVER (ORDER BY date, hour) AS lag_1,
       AVG(price) OVER (ORDER BY date, hour ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS rolling_mean_3
FROM electricity_prices
ORDER BY date, hour
LIMIT 10;

-- Query 12
SELECT date,
       hour,
       price,
       LAG(price,24) OVER (ORDER BY date, hour) AS lag_24,
       AVG(price) OVER (ORDER BY date, hour ROWS BETWEEN 24 PRECEDING AND 1 PRECEDING) AS rolling_mean_24
FROM electricity_prices
ORDER BY date, hour
LIMIT 30;

-- Query 13
WITH price_changes AS(
SELECT date,
       hour,
       price,
       LAG(price,1) OVER (ORDER BY date, hour) AS previous_price
FROM electricity_prices
)


SELECT date,
       hour,
       price,
       previous_price,
       ROUND(price-previous_price,2) AS price_change
FROM price_changes
WHERE price_change < -20
ORDER BY price_change ASC;
