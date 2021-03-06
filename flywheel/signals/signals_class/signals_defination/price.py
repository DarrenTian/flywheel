from flywheel.utils.utils import valid_market_dates
from flywheel.signals.signals_class.signals_defination.signal_interface import signal


class price(signal):

    def __init__(self, name):
        super().__init__(name)

    # get price for single date
    def get_value(self, ticker, date):
        return self.db.get_data(ticker, self.name, date)

    # get price for multi date
    # Output format is dataframe
    def get_multidate_value(self, ticker, dates):
        return self.db.get_multidate_datas(ticker, 'close', dates)

    # get N days ema end of date.
    def ema(self, ticker, date, N):
        valid_dates = valid_market_dates(date, N)
        prices_df = self.get_multidate_value(ticker, valid_dates)
        prices = prices_df['close'].tolist()

        # calculate ema
        n = 0
        ema_t0 = 0
        for price in reversed(prices):
            n = n + 1
            alpha = 2.0 / (n + 1)
            ema_t1 = ema_t0 + alpha * (price - ema_t0)
            ema_t0 = ema_t1
        return ema_t0

    # get Relative Strength Index
    def rsi(self, ticker, date):
        valid_dates = valid_market_dates(date, 15)
        prices_df = self.get_multidate_value(ticker, valid_dates)
        prices = prices_df['close'].tolist()

        sum_past_14_gain = 0.0
        sum_past_14_loss = 0.0
        for i in range(1, 15):
            dif = prices[i] - prices[i - 1]
            if (dif > 0):
                sum_past_14_gain = sum_past_14_gain + dif
            else:
                sum_past_14_loss = sum_past_14_loss - dif

        if (sum_past_14_loss != 0):
            rs = sum_past_14_gain / sum_past_14_loss
        else:
            rs = 100.0
        rsi = 100.0 - 100.0 / (1 + rs)
        return rsi


