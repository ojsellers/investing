#!/usr/bin/python3
'''
@Author = Ollie
'''

from visualisation import *

'''holdings for stocks currently in portfolio with date of first purchase
and quantity bought on first purchase not taking cash value into account
- further purchases are added to holdings as new entry with number after ticker
- base_df (FTSE 100 tracker) and risk_free_df (UK Gilds) stocks are pre
  downloaded and stored in databases to improve analysis speed
[ticker, date, buy_value]'''
holdings = np.array([['SMT_L', '2019-09-23', 100],
                    ['PHGP_L', '2019-09-23', 100],
                    ['CLDN_L', '2019-09-24', 100],
                    ['PNL_L', '2020-03-13', 100],
                    ['ULVR_L', '2020-04-07', 100],
                    ['TMPL_L', '2020-04-07', 100],
                    ['SSON_L', '2020-04-07', 100],
                    ['CLDN_L2', '2020-04-07', 100],
                    ['RCP_L', '2020-04-16', 100],
                    ['ISF_L', '2019-09-23', None],     #base_df FTSE 100 tracker
                    ['GLTS_L', '2019-09-23', None]])    #risk_free_df UK Gilds

'''prospect for stocks of interest in same format as holdings, can specify
start_date or as None and data will be taken from past 5 years. If start_date
is initially None it can then be changed to a date within last 5 years and the
analysis will be done in that time frame'''
prospects = np.array([['GGP_L', None, None],
                    ['LWDB_L', None, None],
                    ['TSLA', None, None],
                    ['AAPL', None, None],
                    ['TSCO_L', None, None],
                    ['PHAG_L', None, None],
                    ['ISF_L', None, None],      #base_df
                    ['GLTS_L', None, None]])    #risk_free_df

test_program()

holdings_db = database_connection('holdings')
prospects_db = database_connection('prospects')

for i in range(len(holdings)):
    print(holdings[i,0])
    #holdings_db.remove_table(holdings[i,0])
    holdings_db.create_update_table(holdings[i,0], holdings[i,1])

for j in range(len(prospects)):
    print(prospects[j,0])
    #prospects_db.remove_table(prospects[j,0])
    prospects_db.create_update_table(prospects[j,0], prospects[j,1])

holdings_db.create_update_overview_table(holdings[:,0], holdings[:,1],
                                                                holdings[:,2])

plot(holdings[:,0], holdings[:,1], 'Returns', holdings_db, scale='linear')
pie('overview', holdings_db)
bar('overview', ['beta', 'alpha', 'sharpes'], holdings_db, 'linear', 1)
bar('overview', ['buy_value', 'current_value'], holdings_db, 'log', 1)
metrics_table('overview', holdings_db)

prospects_db.create_update_overview_table(prospects[:,0], prospects[:,1],
                                                                prospects[:,2])

plot(prospects[:,0], prospects[:,1], 'ReturnsMA', prospects_db, scale='log')
bar('overview', ['beta', 'alpha', 'sharpes'], prospects_db, 'linear', 1)
bar('overview', ['buy_value', 'current_value'], prospects_db, 'log', 1)
metrics_table('overview', prospects_db)
