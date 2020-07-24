from datetime import datetime, timedelta

import yfinance as yf


def get_stock_history_prices(
        ticker: str,
        start: datetime.date = (datetime.now() - timedelta(weeks=1)).date(),
        end: datetime.date = datetime.now().date(),
        **kwargs) -> dict:
    stock = yf.Ticker(ticker)
    stock_history_prices = stock.history(
        start=datetime.strftime(start, '%Y-%m-%d'),
        end=datetime.strftime(end, '%Y-%m-%d'), **kwargs)
    stock_history_prices.index = stock_history_prices.index.to_series().apply(lambda x: str(x)[:10])
    return stock_history_prices.to_dict('index')
