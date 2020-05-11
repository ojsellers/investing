'''
@Author = Ollie
'''

from analysis import *
from sqlalchemy import create_engine

class database_connection():
    def __init__(self, database_name):
        '''This class represents a connection to the mysql database

        :param database_name: the name of database to create or connect to'''
        self.engine = create_engine('mysql://root:daytraders@localhost')
        self.engine.execute(("""CREATE DATABASE IF NOT EXISTS {0};
                                                    """).format(database_name))
        self.engine = create_engine(("""mysql://root:daytraders@localhost/{0}
                                                    """).format(database_name))

    def create_update_table(self, ticker, start_date, mov_avgs):
        '''Fn to create new table for a particular stock ticker from a
        start_date (if None will be 5 years ago)

        :param mov_avgs: True or False to include movin avgs of returns'''
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
        try:
            new = stock_dataframe(ticker, start_date, pd.DataFrame())
            new.new_stock_df(mov_avgs).to_sql(ticker, con=self.engine)
        except:
            return False
        else:
            return True

    def update_table(self, ticker, mov_avgs):
        try:
            current = self.read_dataframe(ticker)
            if current.index.max() == np.busday_offset(date.today() + timedelta(
                                                days=1), -1, roll='backward'):
                return True
            to_date = stock_dataframe(ticker, current.index.max()+timedelta(days
                                    =1), pd.DataFrame()).new_stock_df(mov_avgs)
            updt = stock_dataframe(ticker, None, pd.concat([current, to_date]))
            updt.returns()
            if mov_avgs:
                update.moving_averages()
            self.remove_table(ticker)
            updt.df.to_sql(ticker, con=self.engine)
        except:
            return False
        else:
            return True

    def remove_table(self, ticker):
        try:
            self.engine.execute(("DROP TABLE {0}").format(ticker))
        except:
            print("Table doesn't exist")
            return False
        else:
            print("Table removed")
            return True

    def read_dataframe(self, ticker):
        return pd.read_sql_table(ticker, con=self.engine, index_col='Date')

    def create_update_overview_table(self, tickers, start_date, buy_value):
        '''Fn to generate a table that summarises the stocks in the database
        using functions from the analysis file. These calcs use the returns of
        the stock in question and calc metrics comparing to a baseline
        (FTSE 100 tracker) and risk free (UK Gilds) returns

        :param ticker: list of stock codes in SQL friendly format
        :param start_date: date from which to perform statistical analysis, can
                            None and will be done from start of stock data in db
        :param buy_value: value of stock when purchased
        :return: the dataframe associated with the new SQL overview table'''
        overview_df = pd.DataFrame(columns=['ticker', 'buy_value',
                                'current_value', 'beta', 'alpha', 'sharpes'])
        base_df = self.read_dataframe(tickers[-2])
        risk_free_df = self.read_dataframe(tickers[-1])
        for i in range(len(tickers)-2):
            stock_df = self.read_dataframe(tickers[i])
            if start_date[i]:
                stock_df = update_returns(start_date[i], stock_df)
            prices = get_investment_values(stock_df, buy_value[i])
            metrics = get_metrics(stock_df, start_date[i], base_df,risk_free_df)
            overview_df = self.append(overview_df, tickers[i], prices, metrics)
        overview_df = self.averages_row(overview_df)
        overview_df.to_sql('overview', con=self.engine, if_exists='replace',
                                                                    index=False)
        return overview_df

    def append(self, df, ticker, prices, metrics):
        '''Fn that appends a new row to the overview_df (df) dataframe

        :param prices: 2 element list with 'buy_value and current_value
        :param metrics: 3 element list with beta, alpha and sharpes ratio'''
        return df.append({'ticker': ticker, 'buy_value': prices[0],
                        'current_value': prices[1], 'beta': metrics[0],
                        'alpha': metrics[1], 'sharpes': metrics[2]},
                        ignore_index=True)

    def averages_row(self, df):
        '''Fn to create a row in the overview_df for weighted averages of
        analysis results'''
        total_prices = [np.sum(df['buy_value']), np.sum(df['current_value'])]
        sum_metrics = [np.average(df['beta'], weights = df['current_value']),
                    np.average(df['alpha'], weights = df['current_value']),
                    np.average(df['sharpes'], weights = df['current_value'])]
        return self.append(df, 'Portfolio', total_prices, sum_metrics)

def test_database(ticker, start_date):
    '''Testing the database_connection class by establishing a connection to a
    test database and performing some simple function tests'''
    print('testing database...')
    test_db = database_connection('test')
    test_db.create_update_table(ticker, start_date, True)
    df = test_db.read_dataframe(ticker)
    assert(24<=len(df)<=26)
    assert(len(df.columns)) == 8
    test_db.remove_table(ticker)
    try:
        df = test_db.read_dataframe(ticker)
    except:
        return print('...database testing passed')
    else:
        return print('...database testing failed')

def test_program():
    '''Function runs through data and database test functions and then performs
    some known case assertions on analysis functions'''
    ticker, df, start_date = test_data()
    test_database(ticker, start_date)
    print('testing analysis...')
    rf = risk_free_rate(start_date, df)
    beta_value = beta(covariance(df, df['Returns']))
    assert(beta_value == 1)
    assert(alpha(df, beta_value, rf, df['Returns']) == 0)
    assert(sharpes(df, rf) == 0)
    return print('...analysis testing passed')
