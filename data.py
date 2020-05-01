'''
@Author = Ollie
'''

import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
import pandas as pd
from datetime import datetime, timedelta, date

class data_frame():
    def __init__(self, ticker, start_date, df):
        '''This class represents a dataframe that can be used to scrape up to
        date market data from yfinance api
        param ticker: the code used to represent the stock
        param start_date: the date from which the market data should be gathered
                          can be set to None and will download past 5 years
        param df: can input pre created dataframe to use clean and returns fns
        '''
        self.ticker = ticker.replace("_", ".")
        self.start_date = start_date
        self.df = df

    def download_data(self):
        '''This fn is called to download market data using class params
        return: the downloaded dataframe'''
        if  not self.start_date:
            self.start_date = datetime.today() - timedelta(days=1825)
        self.df = pdr.get_data_yahoo(self.ticker, self.start_date,
                                                            datetime.today())
        self.df.columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
        return self.df

    def clean_data(self):
        '''This fn used to clean downloaded data from yfinance
        - resamples to business days
        - interpolates missing values
        - converts all prices to pence
        return: cleaned dataframe'''
        self.df[self.df.index.dayofweek < 5]
        self.df.interpolate(method='spline', order=3)
        for i in range(len(self.df) - 1):
            for j in range(len(self.df.columns) - 1):
                if (0.1 > self.df.iloc[i+1][j] / self.df.iloc[i][j]):
                    self.df.iat[i+1, j] = self.df.iloc[i+1][j] * 100
                elif (self.df.iloc[i+1][j] / self.df.iloc[i][j] > 10):
                    if not self.update_previous(i, j):
                        return False
        return self.df

    def update_previous(self, i, j):
        '''Fn backtracks up column to update all prices to pence
        param i: row from which backtracking should start (inclusive)
        param j: column which needs backtracking
        return: True or False depending on whether operation was successful'''
        try:
            for x in range(i + 1):
                self.df.iat[x, j] = self.df.iloc[x][j] * 100
        except:
            return False
        else:
            return True

    def returns(self):
        '''Fn to create cumulative returns column using class params
        return: new dataframe with 'Returns' column included'''
        if 'Returns' in self.df:
            del self.df['Returns']
        self.df['Returns'] = (self.df['AdjClose'].pct_change() + 1).cumprod()
        self.df.iat[0, len(self.df.columns) - 1] = 1
        return self.df
