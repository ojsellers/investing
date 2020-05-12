'''
@Author = Ollie
'''

from data import *
import numpy as np

'''
This file contains functions that can be used to analyse stock returns
against a baseline stock (FTSE 100 tracker) and risk free stock (UK Gilds).

Functions calculate 3 different metrics:
- beta: volatility of stock compared to base through covariance matrix of stock
and baseline returns
- alpha: percentage with which stock outperforms market using beta value, risk
free rate of returns, and baseline stock returns
- Sharpes ratio: a single metric accounting for risk and reward calculated by
taking away risk free return from stock return and dividing by standard
deviation of the stock return
'''

def update_returns(start_date, df):
    '''This is used to update the returns column of a dataframe by resampling
    from a specified date using the stock_dataframe class. This is mainly used
    so ISF_L and GLTS_L databases can be resized for comparison with stocks
    having different time frames

    :param start_date: is the date from which resampling should be done
    :param df: dataframe on which recalculating should be performed
    :return: resampled dataframe'''
    return stock_dataframe("",None,df[df.index>=start_date]).pre_process(False)

def risk_free_rate(start_date, risk_free_df):
    return  (update_returns(start_date, risk_free_df)['Returns']).tail(1) - 1

def covariance(df, base):
    return np.cov(df['Returns'], base)

def beta(cov_matrix):
    if cov_matrix[1][1] == 0:
        return np.nan
    return (cov_matrix[0][1] / cov_matrix[1][1])

def alpha(df, beta_value, rf, base):
    a = (df['Returns'].tail(1) - 1) - rf - beta_value * ((base.tail(1)-1) - rf)
    return a.iloc[0] * 100

def sharpes(df, rf):
    if np.std(df['Returns']) == 0:
        return np.nan
    return (((df['Returns'].tail(1) - 1) - rf) / np.std(df['Returns'])).iloc[0]

def get_metrics(df, start_date, base_df, risk_free_df):
    if not start_date:
        start_date = df.head(1).index[0]
    rf = risk_free_rate(start_date, risk_free_df)
    base = update_returns(start_date, base_df)['Returns']
    beta_value = beta(covariance(df, base))
    return beta_value, alpha(df, beta_value, rf, base), sharpes(df, rf)

def get_investment_values(df, buy_value):
    '''This returns buy and current value of stock if buy value is specified,
    if not buy_value is set to 1 and current is relative change '''
    if buy_value != None:
        current_value = ((df['Returns']).iloc[-1]) * float(buy_value)
    else:
        buy_value = (df['Returns']).iloc[0]
        current_value = (df['Returns']).iloc[-1]
    return buy_value, current_value
