'''
@Author = Ollie
'''

import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date

class data_frame():
    '''object represents pandas data_frame for the specified ticker, can
    download data from specified start_date (< 2y ago) '''
    def __init__(self, ticker, start_date, df):
        self.ticker = ticker
        self.start_date = start_date
        self.df = df

    '''Fn to retrieve data to update existing entry or start new entry'''
    def download_data(self):
        if  not self.start_date:
            self.start_date = datetime.today() - timedelta(days=720)
        self.df = pdr.get_data_yahoo(self.ticker, self.start_date, datetime.today())
        self.df.columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
        return self.df

    '''Fn to clean df by resampling to business days, interpolate missing values
    and to ensure the denomination is consistently in pence'''
    def clean_data(self):
        self.df[self.df.index.dayofweek < 5]
        self.df.interpolate(method='spline', order=3)
        for i in range(len(self.df) - 1):
            for j in range(len(self.df.columns)):
                if (0.5 > self.df.iloc[i+1][j] / self.df.iloc[i][j]):
                    self.df.iat[i+1, j] = self.df.iloc[i+1][j] * 100
                elif (self.df.iloc[i+1][j] / self.df.iloc[i][j] > 2):
                    self.df.iat[i, j] = self.df.iloc[i][j] * 100
        return self.df

    '''Fn to add or update a column in df for cumulative returns'''
    def returns(self):
        if 'Returns' in self.df:
            del self.df['Returns']
        self.df['Returns'] = (self.df['AdjClose'].pct_change() + 1).cumprod()
        self.df.iat[0, len(self.df.columns) - 1] = 1
        print(self.df.isna().sum())
        return self.df
