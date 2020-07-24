import datetime
from datetime import timedelta
import pandas as pd

from flywheel.market import market
from flywheel.strategy.account import Account
from flywheel.strategy.strategy import DoNothingStrategy, PortfolioRebalanceStrategy

def backtesting(strategy, start_date, end_date):    
    # account = Account("DUMMY_ACCOUNT")
    # portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"GOOG": 0.5, "PINS": 0.5})
    # account.set_strategy(portfolio_rebalance_strategy)
    # account.add_cash(10000)

    # start_date = datetime.datetime(2020, 1, 1)
    # end_date = datetime.datetime(2020, 2, 1)
    # day_range = (end_date - start_date).days
    # for day in range(day_range):
    #     date = start_date + timedelta(days=day)
    #     market.set_date(date)
    #     account.trade()
    #     #account.show()
    # # This should generate a pandas series
    # # pandas pct_change() will generate a sequence in terms of pct
    # # test
    returns = pd.Series([100, 150, 120])
    return returns.pct_change().fillna(0)

def evaluate(strategy, start_date, end_date):
    returns  = backtesting(strategy, start_date, end_date)    
    metrics = {}
    metrics['Total Return'] = returns.sum()
    # TODO: Max DrawDown, Volatility, Expected Daily/Monthly/Yearly, Daily Value-at-Risk
    return metrics

if __name__ == "__main__":
    portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"GOOG": 0.5, "PINS": 0.5})
    metrics = evaluate(portfolio_rebalance_strategy, '01/01/2020', '02/01/2020')
    for metric in metrics:
        print("{}:{}".format(metric, metrics[metric]))