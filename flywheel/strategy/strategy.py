import math

class Action:
    def __init__(self, action_type={}, action_value={}):
        self.action_type = action_type
        self.action_value = action_value

class Operation:
    def __init__(self, ticker, position, action={}):
        self.ticker = ticker
        self.position = position
        self.action = action

class Strategy:
    def __init__(self):
        pass
    
    def get_operations(self, account):
        pass

class DoNothingStrategy(Strategy):
    def __init__(self):
        pass
    
    def get_operations(self, account):
        return []

class BaseMomentum(Strategy):
    def __init__(self):
        pass

    def get_operations(self, account):
        return []

    def get_longterm_trend(self, signals):
        pass

    def get_fluctuation_range(self, signals):
        pass

    def get_shortterm_trend(self, signals):
        pass

    def get_trend_onging_possibility(self, signals)：
        pass

class PortfolioRebalanceStrategy(Strategy):
    def __init__(self, portfolio_dist, min_rebalance_position=1):
        self.portfolio_dist = portfolio_dist
    
    def get_operations(self, account):
        operations = []
        holdings_equity = 0
        for ticker in account.holdings:
            holdings_equity += account.holdings[ticker] * account.market.get_price(ticker)
        all_equity = account.cash + holdings_equity
        target_holdings = {}
        for ticker in self.portfolio_dist:
            target_holdings[ticker] = math.floor(all_equity * self.portfolio_dist[ticker] / account.market.get_price(ticker))
        for ticker in target_holdings:
            if target_holdings[ticker] != account.holdings[ticker]:
                operations.append(Operation(ticker, target_holdings[ticker]-account.holdings[ticker]))
        return operations