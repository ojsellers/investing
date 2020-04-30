'''
@Author = Ollie
'''

from database import *

'''holdings for stocks currently in portfolio with date of first purchase
and quantity bought on first purchase'''
holdings = [['SMT.L', '2019-09-23', 94],
            ['PHGP.L', '2019-09-23', 8],
            ['CLDN.L', '2019-09-24', 16],
            ['PNL.L', '2020-03-13', 1],
            ['ULVR.L', '2020-04-07', 11],
            ['TMPL.L', '2020-04-07', 74],
            ['SSON.L', '2020-04-07', 57],
            ['RCP.L', '2020-04-16', 43]]

further_purchases = ['CLDN.L', '2020-04-07', 19]

potentials = ['GGP.L', 'LWDB.L', 'TSLA', 'AAPL', 'TSCO.L', 'PHAG.L']

for i in range(len(holdings)):
    check_for_update = data_base_connection(holdings[i][0], holdings[i][1])
    check_for_update.remove_table()
    check_for_update.create_table()

def plot_cumulative_returns(holdings, variable):
    for i in range(len(holdings)):
        data = data_base_connection(holdings[i][0], None)
        for_plot = data.read_data()
        for_plot[variable].plot(label=holdings[i][0])
    plt.xlabel('Date')
    plt.ylabel(variable)
    plt.yscale('log')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
    plt.show()

plot_cumulative_returns(holdings, 'Returns')
