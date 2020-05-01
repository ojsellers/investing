#!/usr/bin/python3
'''
@Author = Ollie
'''

from analysis import *

'''holdings for stocks currently in portfolio with date of first purchase
and quantity bought on first purchase
[ticker, date, quantity]'''
holdings = [['SMT_L', '2019-09-23', 94],
            ['PHGP_L', '2019-09-23', 8],
            ['CLDN_L', '2019-09-24', 16],
            ['PNL_L', '2020-03-13', 1],
            ['ULVR_L', '2020-04-07', 11],
            ['TMPL_L', '2020-04-07', 74],
            ['SSON_L', '2020-04-07', 57],
            ['RCP_L', '2020-04-16', 43]]

further_purchases = ['CLDN.L', '2020-04-07', 19]

prospects = [['GGP_L', None, None],
            ['LWDB_L', None, None],
            ['TSLA', None, None],
            ['AAPL', None, None],
            ['TSCO_L', None, None],
            ['PHAG_L', None, None]]

holdings_db = data_base_connection('holdings')
prospects_db = data_base_connection('prospects')

for i in range(len(holdings)):
    holdings_db.create_table(holdings[i][0], holdings[i][1])

for j in range(len(prospects)):
    prospects_db.create_table(prospects[j][0], prospects[j][1])

plot(holdings, 'Returns', holdings_db)
plot(prospects, 'Returns', prospects_db)
