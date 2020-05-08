'''
@Author = Ollie
'''

from data import *
import matplotlib.pyplot as plt
import numpy as np

def download_df(ticker, start_date, mov_avgs):
    '''Fn to download dataframe with instance of data_frame class
    param ticker: is stock code
    param start_date: is date to download data from to present, can be None
    return: cleaned stock price dataframe with returns column'''
    data = data_frame(ticker, start_date, pd.DataFrame())
    data.download_data()
    data.clean_data()
    data.returns()
    if mov_avgs == True:
        data.moving_averages()
    return data.df

def risk_free_rate(start_date, baseline="GLTS.L"):
    return  download_df(baseline, start_date, False)['Returns'].tail(1) - 1

def bench_mark(start_date, baseline="^FTSE"):
    return  download_df(baseline, start_date, False)['Returns']#.tail(1) - 1

def covariance(df, baseline):
    return np.cov(df, baseline)

def beta(cov_matrix):
    return cov_matrix[0][1]

def alpha(ticker, bench_mark, database):
    pass
