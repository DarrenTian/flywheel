from .factor_interface import factor

class price(factor):

    def __init__(self, name):
        super().__init__(name)

    # get price for single date
    def get_value(self, ticker, date):
        return self.db.get_data(ticker, self.name, date)

    # get price for multi date
    # Output format is dataframe
    def get_multidate_value(self, ticker, dates):
        return self.db.get_multidate_datas(ticker, 'close', dates)