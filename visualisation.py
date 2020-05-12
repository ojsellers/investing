'''
@Author = Ollie
'''

from database import *
import matplotlib.pyplot as plt

def plot(tickers, start_dates, variable, database, scale):
    '''Fn to plot time series for specfied variable and stock
    :param tickers: stock codes to use for plot
    :param variable: particular information to be plotted e.g. 'Returns'
    :param database: a database_connection class to be used to gather data
    :param scale: specify a log or linear y scale
    '''
    for i in range(len(tickers)-2):
        for_plot = database.read_dataframe(tickers[i], 'Date')
        if start_dates[i]:
            for_plot = update_returns(start_dates[i], for_plot)
        for_plot[variable].plot(label=tickers[i])
    plt.xlabel('Date')
    plt.ylabel(variable)
    plt.yscale(scale)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
    plt.show()

def pie(ticker, database):
    '''Creates a pie chart showing the percentage investment in each stock'''
    for_plot = database.read_dataframe(ticker, 'ticker')
    for_plot.drop(for_plot.tail(1).index, inplace=True)
    for_plot['current_value'].plot.pie(subplots=True, autopct='%.2f')
    plt.title('Investments distribution')
    plt.show()

def bar(ticker, columns, database, scale, bar_width):
    '''Creates a bar chart for analysis or values and metrics from overview db
    :param columns: variables to plot
    :bar_width: width of bars on chart'''
    for_plot = database.read_dataframe(ticker, 'ticker')
    for_plot[columns].plot.bar(width=bar_width)
    plt.yscale(scale)
    plt.show()

def metrics_table(ticker, database):
    '''Generates a nice matplotlib table showing overview table'''
    for_plot = database.read_dataframe(ticker, 'ticker').reset_index()
    print(for_plot.head())
    table_text = []
    for_plot = for_plot.round(2)
    for row in range(len(for_plot)):
        table_text.append(for_plot.iloc[row])
    table = plt.table(cellText=table_text, colLabels=for_plot.columns, loc='center')
    table.set_fontsize(45)
    plt.show()
