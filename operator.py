#!/usr/bin/python3
'''
@Author = Ollie
'''

from visualisation import *

'''holdings for stocks currently in portfolio with date of first purchase
and quantity bought on first purchase not taking cash value into account
- further purchases are added to holdings as new entry with number following
ticker that can be combined with original at a later date
[ticker, date, quantity]'''
holdings = [['SMT_L', '2019-09-23', 94],
            ['PHGP_L', '2019-09-23', 8],
            ['CLDN_L', '2019-09-24', 16],
            ['PNL_L', '2020-03-13', 1],
            ['ULVR_L', '2020-04-07', 11],
            ['TMPL_L', '2020-04-07', 74],
            ['SSON_L', '2020-04-07', 57],
            ['CLDN_L2', '2020-04-07', 19],
            ['RCP_L', '2020-04-16', 43]]

prospects = [['GGP_L', None, None],
            ['LWDB_L', None, None],
            ['TSLA', None, None],
            ['AAPL', None, None],
            ['TSCO_L', None, None],
            ['PHAG_L', None, None]]

holdings_db = database_connection('holdings')
prospects_db = database_connection('prospects')

for i in range(len(holdings)):
    #holdings_db.remove_table(holdings[i][0])
    holdings_db.create_update_table(holdings[i][0], holdings[i][1], False)

for j in range(len(prospects)):
    #prospects_db.remove_table(prospects[j][0])
    prospects_db.create_update_table(prospects[j][0], prospects[j][1], True)

a = covariance(holdings_db.read_dataframe("PHGP_L")['Returns'], bench_mark('2019-09-23'))

print(beta(a))

print(risk_free_rate('2019-05-05'))

#plot(holdings, 'Returns', holdings_db)
#plot(prospects, 'ReturnsMA', prospects_db)
