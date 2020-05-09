'''
@Author = Ollie
'''

from data import *
import matplotlib.pyplot as plt
import numpy as np

def risk_free_rate(start_date, baseline="GLTS.L"):
    df = stock_dataframe(baseline, start_date, pd.DataFrame())
    return  df.new_stock_df(False)['Returns'].tail(1) - 1

def bench_mark(start_date, baseline="^FTSE"):
    df = stock_dataframe(baseline, start_date, pd.DataFrame())
    return  df.new_stock_df(False)['Returns']#.tail(1) - 1

def covariance(df, baseline):
    return np.cov(df, baseline)

def beta(cov_matrix):
    return cov_matrix[0][1]

def alpha(ticker, bench_mark, database):
    pass
