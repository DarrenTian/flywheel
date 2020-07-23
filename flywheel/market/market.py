import yfinance as yf
import json

from datetime import date

market_date = date.today()

def set_date(date):
    global market_date
    market_date = date

def get_price_on_date(ticker, date):
    return get_price(ticker, date)

def get_price(ticker):
    print("Get price for {} on {}".format(ticker, market_date))
    market_date_format = str(market_date)[:10]

    with open('stock_data.json', 'r') as json_file:
        stock_data = json.load(json_file)
        if ticker not in stock_data or market_date not in stock_data[ticker]:
            return update_stock_data(stock_data, ticker, market_date_format)
        else:
            return stock_data[ticker][market_date_format]

def update_stock_data(stock_data, ticker, market_date_format):
    stock = yf.Ticker(ticker)
    stock_history_price_dict = crawl_stock_history_price(stock, "10d", "1d")

    # overwrites ticker history price data, updates the stock data and stores as json file
    stock_data[ticker] = stock_history_price_dict
    with open('stock_data.json', 'w') as json_file:
        json.dump(stock_data, json_file, indent=4)
    return stock_data[ticker][market_date_format]

def crawl_stock_history_price(stock_ticker, period="10d", interval="1d"):
    ticker_history_price = stock_ticker.history(period=period, interval=interval)
    ticker_history_price.index = ticker_history_price.index.to_series().apply(lambda x: str(x)[:10])
    print(ticker_history_price)
    return ticker_history_price.to_dict('index')