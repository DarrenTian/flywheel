import yfinance as yf


class factor:

    def __init__(self):
        stock_lists = open("stock_list", "r").read()
        self.stock_index = {}
        for ind, str in enumerate(stock_lists.split('\n')):
            self.stock_index[str] = ind
        self.stocks = yf.Tickers(stock_lists)

    def get_factor(self, stock_name='MSFT'):
        stock = self.stocks.tickers[self.stock_index[stock_name]]
        return stock.history(period="30d", interval="60m")


# f = factor()
# s = f.get_factor()
# print(s)
# print(type(s))
