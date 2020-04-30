'''
@Author = Ollie
'''

from sqlalchemy import create_engine
from data import *

class data_base_connection():
    '''object represents connection to sql data_base that mirrors the pandas
    data_frame object for input ticker to create table, need to update
    user and password for use with different sql servers'''
    def __init__(self, ticker, start_date):
        self.engine = create_engine('mysql://root:daytraders@localhost')
        self.engine.execute('CREATE DATABASE IF NOT EXISTS stocks;')
        self.engine = create_engine('mysql://root:daytraders@localhost/stocks')
        self.ticker = (ticker[:3] + (ticker[3:] and ''))
        self.ticker_for_df = ticker
        self.start_date = start_date

    '''Fn to check if a table for the ticker exists and, if not, create one '''
    def create_table(self):
        try:
            self.engine.execute(("""SELECT 1 FROM {0}
                                                LIMIT 1""").format(self.ticker))
        except:
            if self.new_table():
                print('New table created')
                return True
            else:
                print('Unable to create table')
                return False
        else:
            if self.update_table():
                print("Table updated")
                return True
            else:
                print('Unable to update table')
                return False

    '''Fn to download data_frame from specified start_date'''
    def download_df(self, start_date):
        data = data_frame(self.ticker_for_df, start_date, pd.DataFrame())
        data.download_data()
        data.clean_data()
        data.returns()
        return data.df

    '''Fn called if no sql table for ticker previously exists, downloads data'''
    def new_table(self):
        try:
            self.download_df(self.start_date).to_sql(self.ticker,
                                                                con=self.engine)
        except:
            return False
        else:
            return True

    '''Fn called if sql table for ticker exists, updates data to current date'''
    def update_table(self):
        try:
            current = self.read_data()
            if current.index.max() == date.today():
                return True
            update = data_frame(self.ticker_for_df, False, pd.concat([current,
                                self.download_df(current.index.max() +
                                timedelta(days=1))]))
            update.returns()
            self.remove_table()
            update.df.to_sql(self.ticker, con=self.engine)
        except:
            return False
        else:
            return True

    '''Fn to remove sql table for ticker'''
    def remove_table(self):
        try:
            self.engine.execute(("DROP TABLE {0}").format(self.ticker))
        except:
            print("Table doesn't exist")
        else:
            print("Table removed")

    def read_data(self):
        return pd.read_sql_table(self.ticker, con=self.engine, index_col='Date')
