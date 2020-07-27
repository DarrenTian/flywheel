from datetime import datetime, timedelta
from typing import List

from flywheel.exceptions import UserError
from flywheel.models import Stock, StockPrice


def get_stock_prices(
        ticker: str,
        start: datetime.date = (datetime.now() - timedelta(weeks=1)).date(),
        end: datetime.date = datetime.now().date()) -> List[dict]:
    stock = Stock.get_by_ticker(ticker)
    if not stock:
        raise UserError(f'{ticker} not found')
    prices = list(StockPrice.select().where(
        StockPrice.stock_id == stock.id,
        StockPrice.date >= start,
        StockPrice.date <= end
    ))
    return [price.to_dict() for price in prices]
