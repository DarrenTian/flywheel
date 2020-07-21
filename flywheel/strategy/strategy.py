import math

from flywheel.market import market

class Operation:
    def __init__(self, ticker, type, position):
        self.ticker = ticker
        self.type = type
        self.position = position

class Strategy:
    def __init__(self):
        pass
    
    def get_operations(self, cash, holdings):
        pass

class DoNothingStrategy(Strategy):
    def __init__(self):
        pass
    
    def get_operations(self, cash, holdings):
        return []

class PortfolioRebalanceStrategy(Strategy):
    def __init__(self, portfolio_dist, min_rebalance_position=1):
        self.portfolio_dist = portfolio_dist
    
    def get_operations(self, cash, holdings):
        operations = []
        holdings_equity = 0
        for ticker in holdings:
            holdings_equity += holdings[ticker] * market.get_price(ticker)
        all_equity = cash + holdings_equity
        target_holdings = {}
        for ticker in self.portfolio_dist:
            target_holdings[ticker] = math.floor(all_equity * self.portfolio_dist[ticker] / market.get_price(ticker))
        for ticker in target_holdings:
            if target_holdings[ticker] < holdings[ticker]:
                operations.append(Operation(ticker, 'SELL', holdings[ticker]-target_holdings[ticker]))
            if target_holdings[ticker] > holdings[ticker]:
                operations.append(Operation(ticker, 'BUY', target_holdings[ticker]-holdings[ticker]))
        return operations