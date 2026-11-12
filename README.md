Equity Market Trends: Volatility Regimes and Valuation Signals
An independent data-analysis project by Tharun Gonela, MSc Data Science student at the University of Roehampton.

This project explores whether simple, transparent market measures—volatility regimes and starting valuations—can provide useful insight into future equity returns. It uses public monthly S&P 500 data and applies Python-based analysis, visualisation, and out-of-sample testing.

Important: This project is for learning and research purposes only. It is not investment advice, does not constitute a trading strategy, and does not represent the views of any employer.

Objective
The main question was:

Can volatility regimes and starting valuation levels provide useful insight into subsequent equity returns, and do these relationships remain useful in an out-of-sample test?

Data
Public monthly S&P 500 dataset from the datasets/s-and-p-500 GitHub repository.

Monthly index levels from 1871 to September 2026.

Real price and CAPE (Cyclically Adjusted Price-to-Earnings) data available up to September 2023.

Zeros in the dataset were treated as missing values.

Returns were calculated as price returns, excluding dividends.

Methods
1. Volatility regime analysis
Calculated monthly returns from S&P 500 index levels.

Computed rolling 12-month realised volatility.

Annualised volatility using the square root of 12.

Identified high-volatility months as the top 20% of rolling volatility observations.

Compared average forward 12-month price returns for high- and low-volatility periods.

2. Valuation analysis
Used CAPE as a long-term valuation measure.

Grouped historical starting points into five CAPE quintiles.

Compared average subsequent 10-year annualised real price returns across valuation groups.

Recognised that overlapping 10-year windows reduce the number of independent observations.

3. Out-of-sample walk-forward test
Built an expanding-window regression model using log CAPE to predict the next 12-month real return.

Used only information available at each point in time.

Compared the model against an expanding-mean baseline.

Tested the model from 1960 to September 2022.

Measured out-of-sample R-squared and cumulative squared-error advantage.

Key findings
Volatility regimes
Months in the top 20% of rolling 12-month volatility were followed by higher average 12-month price returns than other months.

Period	High-volatility months	Other months
1871–2025	8.2% average forward 12-month return	6.1%
Since 1996	16.2%	8.0%
This result is descriptive rather than predictive. High-volatility periods often occur around market drawdowns, which may later be followed by recovery periods.

Starting valuation
Across 1,593 monthly starting points from 1881 to 2013, CAPE and the following 10-year annualised real price return had a correlation of -0.33.

CAPE quintile	Mean next 10-year real return per year
Q1: Cheapest	5.5%
Q2	2.0%
Q3	2.1%
Q4	1.8%
Q5: Most expensive	0.2%
Lower starting valuations were associated with higher long-run average returns, although overlapping windows mean this result should be interpreted cautiously.

Out-of-sample result
The CAPE-based walk-forward model did not outperform a simple expanding-mean baseline.

Period	Out-of-sample R-squared
Overall, 1960–2022	-0.10
1960–1989	+0.02
1990–2022	-0.21
This suggests that a long-horizon relationship between valuation and future returns does not automatically become a reliable short-term forecasting model.

Visualisations
The project includes:

S&P 500 price chart with high-volatility periods highlighted.

CAPE quintile comparison against subsequent 10-year real returns.

Walk-forward model performance against an expanding-mean baseline.

Skills demonstrated
Python

Pandas

NumPy

Matplotlib

Data cleaning

Exploratory data analysis

Time-series analysis

Rolling-window analysis

Volatility calculation

Valuation analysis

Out-of-sample testing

Walk-forward validation

Financial-market research

Data storytelling

Critical interpretation of results

Limitations
The analysis uses one index, the S&P 500.

Returns exclude dividends.

Post-2023 price data was not independently verified.

Monthly average data may smooth volatility.

Rolling and overlapping windows create dependence between observations.

No formal statistical significance testing was included.

No transaction costs, taxes, or trading constraints were considered.

The model is not suitable for live trading or investment decisions.

Future improvements
Add dividend-adjusted total returns.

Include interest rates, inflation, earnings growth, and macroeconomic variables.

Test regime-based models such as Hidden Markov Models.

Use block bootstrap methods to account for overlapping observations.

Extend the analysis to other asset classes and international markets.

Add statistical significance testing and confidence intervals.

Build an interactive dashboard using Streamlit or Power BI.
