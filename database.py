'''
@Author = Ollie
'''

from sqlalchemy import create_engine
from analysis import *

class database_connection():
    def __init__(self, database_name):
        '''This class represents a connection to the mysql database
        param database_name: the name of database to create or connect to'''
        self.engine = create_engine('mysql://root:daytraders@localhost')
        self.engine.execute(("""CREATE DATABASE IF NOT EXISTS {0};
                                                    """).format(database_name))
        self.engine = create_engine(("""mysql://root:daytraders@localhost/{0}
                                                    """).format(database_name))

    def create_update_table(self, ticker, start_date, mov_avgs):
        '''Fn to create new table for a particular DataFrame
        param ticker: is the stock code
        param start_date: date from which data is to be collected, can be None
        return: True or False depending on successful operation'''
        try:
            self.engine.execute(("""SELECT 1 FROM {0}
                                                LIMIT 1""").format(ticker))
        except:
            if self.new_table(ticker, start_date, mov_avgs):
                print('New table created')
                return True
            else:
                print('Unable to create table')
                return False
        else:
            if self.update_table(ticker, mov_avgs):
                print("Table updated")
                return True
            else:
                print('Unable to update table')
                return False

    def new_table(self, ticker, start_date, mov_avgs):
        '''Fn called if no table exists to create new, params same as previous
        return: True or False depending on successful operation'''
        try:
            new = stock_dataframe(ticker, start_date, pd.DataFrame())
            new.new_stock_df(mov_avgs).to_sql(ticker, con=self.engine)
        except:
            return False
        else:
            return True

    def update_table(self, ticker, mov_avgs):
        '''Fn called if sql table exists to update to present date
        param ticker: is stock code
        return: True or False depending on successful operation'''
        try:
            current = self.read_dataframe(ticker)
            if current.index.max() == np.busday_offset(date.today(), -1,
                                                            roll='backward'):
                return True
            to_date =stock_dataframe(ticker, current.index.max()+timedelta(days=1),
                                        pd.DataFrame()).new_stock_df(mov_avgs)
            update = stock_dataframe(ticker, False, pd.concat([current, to_date]))
            update.returns()
            if mov_avgs:
                update.moving_averages()
            self.remove_table(ticker)
            update.df.to_sql(ticker, con=self.engine)
        except:
            return False
        else:
            return True

    def remove_table(self, ticker):
        '''Fn removes table from sql database specified by class variable
        param ticker: stock code
        return: True or False depending on successful operation'''
        try:
            self.engine.execute(("DROP TABLE {0}").format(ticker))
        except:
            print("Table doesn't exist")
            return False
        else:
            print("Table removed")
            return True

    def read_dataframe(self, ticker):
        '''Fn to make copy of database table as a pandas DataFrame
        param ticker: stock code
        return: pandas dataframe of market price data'''
        return pd.read_sql_table(ticker, con=self.engine, index_col='Date')

    def current_returns(self, ticker):
        query = self.engine.execute(("""SELECT Returns FROM {0} S WHERE Date =
                    (SELECT MAX(Date) FROM {0})""").format(ticker))
        return query.fetchall()[0][0] - 1

    def create_update_overview_table(self, tickers):
        self.engine.execute("""CREATE TABLE IF NOT EXISTS 'overview' (
                                                'name' VARCHAR NOT NULL,
                                                'buy_value' DECIMAL,
                                                'current_value' DECIMAL,
                                                'alpha' DECIMAL,
                                                'beta' DECIMAL,
                                                'sharpe_ratio' DECIMAL);""")
        self.engine.execute("""TRUNCATE TABLE 'overview';""")
        for i in range(len(tickers)):
            pass
