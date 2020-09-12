from flywheel.signals.factor.factor import factor


class volume(factor):

    def __init__(self, name):
        super().__init__(name)

    # get volume for single date
    def get_value(self, ticker, date):
        return self.db.get_data(ticker, self.name, date)