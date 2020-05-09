'''
@Author = Ollie
'''

from database import *

def plot(tickers, variable, database):
    '''Fn to plot specified data
    param tickers: stock codes to use for plot
    param variable: particular information to be plotted e.g. 'Returns'
    param database: a database_connection class to be used to gather data'''
    for i in range(len(tickers)):
        for_plot = database.read_dataframe(tickers[i][0])
        for_plot[variable].plot(label=tickers[i][0])
    plt.xlabel('Date')
    plt.ylabel(variable)
    plt.yscale('linear')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
    plt.show()
