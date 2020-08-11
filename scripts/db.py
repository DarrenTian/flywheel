from flywheel.models import *
from flywheel.settings import *
from flywheel.consts import *


def get_all_models():
    import gc
    return [
        kls for kls in gc.get_objects()
        if issubclass(type(kls), type) and issubclass(kls, BaseModel)
        and kls != BaseModel and 'BaseModel' not in kls.__name__
    ]


def create_all_tables():
    db.create_tables(get_all_models())


def drop_all_tables():
    db.drop_tables(get_all_models())


def init_data():
    for stock in STOCK_LIST:
        if Stock.get_by_ticker(ticker=stock) is None:
            Stock.create(ticker=stock, market=Market.NASDAQ)


def init():
    create_all_tables()
    init_data()


if __name__ == '__main__':
    init()
