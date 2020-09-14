from flywheel.signals.factor.factor import factor


class price(factor):

    def __init__(self, name):
        super().__init__(name)

    # get price for single date
    def get_value(self, ticker, date):
        return self.db.get_data(ticker, self.name, date)

    # get price for multi date
    def get_multidate_value(self, ticker, dates):
        return self.db.get_multidate_datas(ticker, self.name, dates)