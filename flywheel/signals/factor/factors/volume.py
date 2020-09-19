from .factor_interface import factor

class volume(factor):

    def __init__(self, name):
        super().__init__(name)

    # get volume for single date
    def get_value(self, ticker, date):
        return self.db.get_data(ticker, self.name, date)

    # get volume for multi date
    # Output format is dataframe
    def get_multidate_value(self, ticker, dates):
        return self.db.get_multidate_datas(ticker, self.name, dates)