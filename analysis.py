'''
@Author = Ollie
'''

from data import *
import matplotlib.pyplot as plt
import numpy as np

def bench_mark(start_date, baseline="^FTSE"):
    df = stock_dataframe(baseline, start_date, pd.DataFrame())
    return  df.new_stock_df(False)['Returns']

def risk_free_rate(start_date, baseline="GLTS.L"):
    return  bench_mark(start_date, baseline).tail(1) - 1

def covariance(df, baseline):
    return np.cov(df, baseline)

def beta(cov_matrix):
    return cov_matrix[0][1] / cov_matrix[1][1]

def alpha(df, risk_free, beta_value):
    return (df.tail(1)-1) - risk_free - beta_value * (benchmark_return - risk_free)

def sharpes():
    pass
