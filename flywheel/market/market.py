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
    return get_price_on_date(ticker, market_date)
