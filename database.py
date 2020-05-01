'''
@Author = Ollie
'''

from sqlalchemy import create_engine
from data import *

class data_base_connection():
    def __init__(self, database_name):
        '''This class represents a connection to the mysql database
        param database_name: the name of database to create or connect to'''
        self.engine = create_engine('mysql://root:daytraders@localhost')
        self.engine.execute(("""CREATE DATABASE IF NOT EXISTS {0};
                                                    """).format(database_name))
        self.engine = create_engine(("""mysql://root:daytraders@localhost/{0}
                                                    """).format(database_name))

    def create_table(self, ticker, start_date):
        '''Fn to create new table for a particular DataFrame
        param ticker: is the stock code
        param start_date: date from which data is to be collected, can be None
        return: True or False depending on successful operation'''
        try:
            self.engine.execute(("""SELECT 1 FROM {0}
                                                LIMIT 1""").format(ticker))
        except:
            if self.new_table(ticker, start_date):
                print('New table created')
                return True
            else:
                print('Unable to create table')
                return False
        else:
            if self.update_table(ticker):
                print("Table updated")
                return True
            else:
                print('Unable to update table')
                return False

    def download_df(self, ticker, start_date):
        '''Fn to download dataframe with instance of data_frame class
        param ticker: is stock code
        param start_date: is date to download data from to present, can be None
        return: cleaned stock price dataframe with returns column'''
        data = data_frame(ticker, start_date, pd.DataFrame())
        data.download_data()
        data.clean_data()
        data.returns()
        return data.df

    def new_table(self, ticker, start_date):
        '''Fn called if no table exists to create new, params same as previous
        return: True or False depending on successful operation'''
        try:
            self.download_df(ticker, start_date).to_sql(ticker, con=self.engine)
        except:
            return False
        else:
            return True

    def update_table(self, ticker):
        '''Fn called if sql table exists to update to present date
        param ticker: is stock code
        return: True or False depending on successful operation'''
        try:
            current = self.read_data(ticker)
            if current.index.max() == date.today():
                return True
            update = data_frame(ticker, False, pd.concat([current,
                            self.download_df(ticker, current.index.max() +
                                                        timedelta(days=1))]))
            update.returns()
            self.remove_table()
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

    def read_data(self, ticker):
        '''Fn to make copy of database table as a pandas DataFrame
        param ticker: stock code
        return: pandas dataframe of market price data'''
        return pd.read_sql_table(ticker, con=self.engine, index_col='Date')
