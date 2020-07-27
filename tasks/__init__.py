import logging
from datetime import datetime, timedelta

from celery import Celery

from flywheel.settings import TZ, REDIS_URI
from flywheel.market.yahoo import get_stock_history_prices
from flywheel.models import StockPrice, Stock
from flywheel.exceptions import UserError

logging.basicConfig(level="INFO", format='%(asctime)-15s [%(levelname)s] [%(name)-9s] %(message)s')

logger = logging.getLogger(__name__)
app = Celery('tasks', broker=REDIS_URI + '//', backend=REDIS_URI)
app.conf.timezone = TZ


@app.task
def crawl_stock_history_data(ticker: str, days=7):
    try:
        stock = Stock.get_by_ticker(ticker)
        if not stock:
            raise UserError(f'stock {ticker} not found')
        logger.info(f'start to crawl {ticker} last {days} days data...')
        prices = get_stock_history_prices(
            ticker,
            start=(datetime.now() - timedelta(days=days)).date(),
            end=datetime.now().date())
        logger.info(f'finished crawl {ticker} data, and start to store in database...')
        StockPrice.bulk_create(
            [StockPrice(
                stock_id=stock.id,
                date=datetime.strptime(date, '%Y-%m-%d'),
                open=price['Open'],
                high=price['High'],
                low=price['Low'],
                close=price['Close'],
                volume=price['Volume'],
                dividends=prices.get('Dividends', 0),
                stock_splits=price.get('Stock Splits', 0)
            ) for date, price in prices.items()],
            batch_size=100
        )
        logger.info(f'crawl {ticker} last {days} days data done.')
    except UserError as e:
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


@app.task
def crawl_all_stock_history_data(days=7):
    stocks = Stock.all()
    for stock in stocks:
        crawl_stock_history_data.delay(ticker=stock.ticker, days=days)
