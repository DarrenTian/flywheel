import yfinance as yf
import json
import sqlite3

from datetime import date
from playhouse.db_url import connect

#DUMMY_DATA_PATH = 'flywheel/market/stock_data.json'
DUMMY_DATA_PATH = 'stock_data.json'

market_date = date.today()

# Dumb implemention telling if it's weekday or not

conn = connect('sqlite:///flywheel.db')
cur = conn.cursor()
if 'MARKET' not in conn.get_tables():
    create_market_table_sql = '''CREATE TABLE MARKET(
       ticket CHAR(10),
       date DATE,
       open FLOAT,
       high FLOAT,
       low FLOAT,
       close FLOAT,
       volume INT,
       dividends FLOAT,
       stock_splits INT,
       PRIMARY KEY (ticket, date)
    )'''
    cur.execute(create_market_table_sql)
    print("Create market table in the database.")


def set_date(date):
    global market_date
    market_date = date


def get_price(ticker):
    # print("Market is Open: {}".format(is_open()))
    # print("Get price for {} on {}".format(ticker, market_date))
    market_date_format = str(market_date)[:10]

    read_sql = '''
        SELECT *
        FROM MARKET
        WHERE ticket = ?
        AND date = ?
    '''

    cur.execute(read_sql, (ticker, market_date_format, ))
    rows = cur.fetchall()

    if len(rows) == 0:
        update_stock_data(ticker, market_date_format)

        # re-query in the DB after update
        cur.execute(read_sql, (ticker, market_date_format,))
        rows = cur.fetchall()

    # the index of close is 5 in DB
    return rows[0][5]


def update_stock_data(ticker, market_date_format):
    stock = yf.Ticker(ticker)
    stock_history_price_dict = crawl_stock_history_price(stock, "10d", "1d")

    # overwrites ticker history price data, updates the stock data and stores in database
    insert_sql = '''
        REPLACE INTO MARKET (ticket, date, open, high, low, close, volume, dividends, stock_splits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    record_list = []
    for key, value in stock_history_price_dict.items():
        record_list.append((ticker, key, value['Open'], value['High'], value['Low'], value['Close'], value['Volume'], value['Dividends'], value['Stock Splits']))
    cur.executemany(insert_sql, record_list)
    conn.commit()
    return stock_history_price_dict[market_date_format]


def crawl_stock_history_price(stock_ticker, period="10d", interval="1d"):
    ticker_history_price = stock_ticker.history(period=period, interval=interval)
    ticker_history_price.index = ticker_history_price.index.to_series().apply(lambda x: str(x)[:10])
    print(ticker_history_price)
    print(ticker_history_price.to_dict('index'))
    return ticker_history_price.to_dict('index')

def is_holiday(date):
    return date.isoformat() in \
        ['2020-01-01', '2020-01-20','2020-02-17','2020-05-25','2020-07-03','2020-07-04','2020-09-07',
         '2020-07-04', '2020-10-12','2020-11-11','2020-11-26','2020-12-25']

class Market:

    # TODO: implement crawling and query function

    def __init__(self):
        self.DUMMY_DATA_PATH = 'flywheel/market/stock_data.json'
        self.market_date = date.today()
        self.period = '2y'
        self.interval = '1d'

    def is_open(self):
        if is_holiday(self.market_date):
            return False
        return self.market_date.isoweekday() in range(1, 5)

    def set_dummy_data_path(self, DUMMY_DATA_PATH):
        self.DUMMY_DATA_PATH = DUMMY_DATA_PATH

    def set_market_date(self, market_date):
        self.market_date = market_date

    def set_period(self, period):
        self.period = period

    def set_interval(self, interval):
        self.interval = interval

    def get_price(self, ticker='MSFT'):
        print("Looking for {} on {}".format(ticker, self.market_date))
        market_date_format = str(self.market_date)[:10]

        with open(self.DUMMY_DATA_PATH, 'r') as json_file:
            stock_data = json.load(json_file)
            if ticker not in stock_data or market_date_format not in stock_data[ticker]:
                return self.update_stock_data(stock_data, ticker, market_date_format)['Close']
            else:
                return stock_data[ticker][market_date_format]['Close']

    def update_stock_data(self, stock_data, ticker, market_date_format):
        stock = yf.Ticker(ticker)
        stock_history_price_dict = crawl_stock_history_price(stock, self.period, self.interval)

        # overwrites ticker history price data, updates the stock data and stores as json file
        stock_data[ticker] = stock_history_price_dict
        with open(self.DUMMY_DATA_PATH, 'w') as json_file:
            json.dump(stock_data, json_file, indent=4)
        return stock_data[ticker][market_date_format]
