import yfinance as yf
import json

from datetime import date

market_date = date.today()

def set_date(date):
    global market_date
    market_date = date

def get_price_on_date(ticker, date):
    # test data
    if ticker == 'GOOG':
        return 100
    if ticker == 'PINS':
        return 50
    return 0

def get_price(ticker):
    print("Get price for {} on {}".format(ticker, market_date))

    with open('stock_data.txt') as json_file:
        stock_data = json.load(json_file)
        if ticker not in stock_data or market_date not in stock_data[ticker]:
            return update_stock_data(ticker)
        else:
            return stock_data[ticker][market_date]


def update_stock_data(ticker, market_date):
    # return the data of stock_data[ticker][date]
    pass