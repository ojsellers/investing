'''
@Author = Ollie
'''

from database import *

portfolio = ['SMT.L', 'PNL.L', 'CLDN.L', 'PHGP.L', 'RCP', 'GGP.L', 'LWDB.L',
            'TMPL.L', 'ULVR.L', 'TSLA', 'AAPL', 'TSCO.L', 'SSON.L', 'PHAG.L']

for i in range(len(portfolio)):
    check_for_update = data_base_connection(portfolio[i])
    check_for_update.create_table()

def plot_cumulative_returns(portfolio, variable):
    for i in range(len(portfolio)):
        data = data_base_connection(portfolio[i])
        for_plot = data.read_data()
        for_plot[variable].plot(label=portfolio[i])
    plt.xlabel('Date')
    plt.ylabel(variable)
    plt.yscale('log')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
    plt.show()

plot_cumulative_returns(portfolio, 'Returns')
