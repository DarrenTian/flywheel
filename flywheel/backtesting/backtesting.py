import datetime
from datetime import date, timedelta
import pandas as pd

from flywheel.backtesting import stats
from flywheel.market import market
from flywheel.strategy.account import Account
from flywheel.strategy.strategy import DoNothingStrategy, PortfolioRebalanceStrategy

def backtesting(strategy, start_date, end_date):    
    account = Account("DUMMY_ACCOUNT")
    portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"BABA": 0.5, "EBAY": 0.5})
    account.set_strategy(portfolio_rebalance_strategy)
    account.add_cash(10000)

    account_snapshot = []
    day_range = (end_date - start_date).days
    for day in range(day_range):
        date = start_date + timedelta(days=day)
        market.set_date(date)
        if market.is_open():
            account.trade()
            account.show()
            account_snapshot.append(account.equity())
    prices = pd.Series(account_snapshot)
    return prices

def calculate_metrics(prices):
    metrics = {}

    returns = prices.pct_change().fillna(0)
    metrics['Total Return'] = stats.total_return(returns)
    metrics['Max DrawDown'] = stats.max_drawdown(prices)
    # TODO: Max DrawDown, Volatility, Expected Daily/Monthly/Yearly, Daily Value-at-Risk
    return metrics


def evaluate(strategy, start_date, end_date):
    end_date = date.today()
    start_date = end_date - timedelta(days=10)
    prices  = backtesting(strategy, start_date, end_date)    
    metrics = calculate_metrics(prices)
    return metrics

if __name__ == "__main__":
    portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"GOOG": 0.5, "PINS": 0.5})
    metrics = evaluate(portfolio_rebalance_strategy, '01/01/2020', '02/01/2020')
    for metric in metrics:
        print("{}:\n{}".format(metric, metrics[metric]))