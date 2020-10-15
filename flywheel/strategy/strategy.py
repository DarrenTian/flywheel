import math

import flywheel.proto_gen.signal.signal_pb2 as Signal
import flywheel.proto_gen.strategy.strategy_pb2 as StrategySet

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
    # only consider 200 ema, momentum indicator, trend, fluctuation range for bootstrap
    # 1. when momentum is singular and fluctuation range broken, strong trade signal
    # 2. above ema -> divergences on the lower side of momentum indicator
    #    e.g. price down(up) trend but momentum got higher high(lower high, both below 0), when cross 0, strong buy signal
    #    below ema -> divergences on the upper side of momentum indicator
    # 3. advanced use 100 ema of momentum to replace 0
    # signals: list of Signal
    self.operation_list = []
    def __init__(self, signals):
        pass

    def get_operations(self, account):
        return self.operation_list

    def get_longterm_trend(self, signals):
        pass

    def get_fluctuation_range(self, signals):
        pass

    def get_shortterm_trend(self, signals):
        pass

    def get_trend_onging_possibility(self, signals):
        pass

    # start with (0, -1, 1) * speed * peak
    def get_critical_point_score(self, indicator, base_line):
        pass

    # start with (0, -X, X) X: hyper-premeters to finetune
    def get_breakthrough_score(self, indicator, range):
        pass

    # normalize function, start with cut only
    def get_normalized_score(self, score):
        if (score < 0):
            return max(-10, score)
        else:
            return min(score, 10)

    # score function: (momentum, ema, trend, fluctuation_range, closing_price) -> [-10, 10]
    # use linear scoring function here, would use ML to determine the diviation to normalize the range
    def get_combined_score(self, ema_200, momentum_indicator, trend, fluctuation_range, closing_price):
        base_score = 0.0
        # base score
        if (trend.type == Signal.Trend.TrendType.UP):
            base_score = 1.0
        else if (trend.type == Signal.Trend.TrendType.DOWN):
            base_score = -1.0

        if (trend.confidence != 0):
            base_score *= trend.confidence

        # momentum score
        momentum_score = get_critical_point_score(momentum_indicator, [])

        # ema score
        ema_score = get_critical_point_score(closing_price, ema_200)

        # range score
        range_score = get_breakthrough_score(closing_price, fluctuation_range)

        # start only trade aline with trend
        if (base_score * momentum_score <= 0):
            return 0.0

        # has breakthrough, shortterm quick trade
        if (momentum_score * range_score > 0):
            return get_normalized_score(base_score * momentum_score * range_score)

        # divergence found
        if (momentum_score * ema_score < 0):
            return get_normalized_score(-1 * base_score * momentum_score * ema_score)

        return 0.0

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