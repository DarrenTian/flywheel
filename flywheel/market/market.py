import yfinance as yf
import json

from datetime import date

DUMMY_DATA_PATH = 'flywheel/market/stock_data.json'

market_date = date.today()

# Dumb implemention telling if it's weekday or not
def is_open():
    return market_date.isoweekday() in range(1, 5)

def set_date(date):
    global market_date
    market_date = date


def get_price(ticker):
    # print("Market is Open: {}".format(is_open()))
    # print("Get price for {} on {}".format(ticker, market_date))
    market_date_format = str(market_date)[:10]

    with open(DUMMY_DATA_PATH, 'r') as json_file:
        stock_data = json.load(json_file)
        if ticker not in stock_data or market_date_format not in stock_data[ticker]:
            return update_stock_data(stock_data, ticker, market_date_format)['Close']
        else:
            return stock_data[ticker][market_date_format]['Close']


def update_stock_data(stock_data, ticker, market_date_format):
    stock = yf.Ticker(ticker)
    stock_history_price_dict = crawl_stock_history_price(stock, "10d", "1d")

    # overwrites ticker history price data, updates the stock data and stores as json file
    stock_data[ticker] = stock_history_price_dict
    with open(DUMMY_DATA_PATH, 'w') as json_file:
        json.dump(stock_data, json_file, indent=4)
    return stock_data[ticker][market_date_format]


def crawl_stock_history_price(stock_ticker, period="10d", interval="1d"):
    ticker_history_price = stock_ticker.history(period=period, interval=interval)
    ticker_history_price.index = ticker_history_price.index.to_series().apply(lambda x: str(x)[:10])
    print(ticker_history_price)
    return ticker_history_price.to_dict('index')

class market:

    # TODO: implement crawling and query function

    def __init__(self):
        self.DUMMY_DATA_PATH = 'flywheel/market/stock_data.json'
        self.market_date = date.today()
        self.period = '10d'
        self.interval = '1d'

    def set_dummy_data_path(self, DUMMY_DATA_PATH):
        self.DUMMY_DATA_PATH = DUMMY_DATA_PATH

    def set_market_date(self, market_date):
        self.market_date = market_date

    def set_period(self, period):
        self.period = period

    def set_interval(self, interval):
        self.interval = interval

    def get_price(self, ticker='MSFT'):
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

