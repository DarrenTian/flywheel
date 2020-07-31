import datetime
from datetime import date, timedelta
import pandas as pd

from flywheel.backtesting import stats
from flywheel.market.market import Market
from flywheel.strategy.account import Account
from flywheel.strategy.strategy import DoNothingStrategy, PortfolioRebalanceStrategy

market = Market()

def backtesting(strategy, start_date, end_date):    
    account = Account("DUMMY_ACCOUNT")
    account.set_strategy(strategy)
    account.add_cash(10000)
    account.set_market(market)

    account_snapshot = []
    day_range = (end_date - start_date).days
    for day in range(day_range):
        date = start_date + timedelta(days=day)
        market.set_market_date(date)
        if market.is_open():
            account.trade()
            account.show()
            account_snapshot.append(account.equity())
    prices = pd.Series(account_snapshot)
    return prices

def evaluate(strategy, start_date, end_date):
    prices  = backtesting(strategy, start_date, end_date)    
    metrics = stats.calculate_metrics(prices)
    return metrics

if __name__ == "__main__":
    # portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"INTC": 0.5, "GOOG": 0.5})
    # prices = backtesting(portfolio_rebalance_strategy, datetime.date(2020, 7, 1), date.today())
    prices = pd.Series([100, 101, 99, 98, 97, 100, 105, 104, 103, 105, 106, 105, 104])
    print(stats.drawdowns(prices))
    print(stats.longest_drawdown_days(prices))

    # metrics = evaluate(portfolio_rebalance_strategy, datetime.date(2020, 7, 1), date.today())
    # for metric in metrics:
    #     print("{}:\n{}".format(metric, metrics[metric]))