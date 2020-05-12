# investing
Keeping track of investments and evaluating new prospects

Done:
- In this project I built an ETL pipeline that scrapes market data using the yfinance API, stores in an SQL database, and performs some statistical portfolio analysis. This analysis is then presented in various visualisations.

File overview:

data.py: 
- the file for scraping and cleaning data from the yfinance API
- uses a stock_dataframe class to allow downloading of up-to-date data for new or existing dataframe
- contains preprocessing functions to clean data, add a returns column, and add moving averages of the returns column

database.py:
- for connecting and creating tables in SQL databases
- uses database_connecction class to represent a connection to a particular mysql database
- contains functions to create new tables from stock price dataframes created in data.py
- also contains functions to generate a portfolio overview table in sql database with metrics

analysis.py:
- contains functions used for metrics calculations

visualisation.py:
- contains functions used for producing visulations

operator.py:
- operation file where info about portfolio is input
