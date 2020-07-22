import datetime
from datetime import timedelta

from flywheel.market import market
from flywheel.strategy.account import Account
from flywheel.strategy.strategy import DoNothingStrategy, PortfolioRebalanceStrategy

def main():    
    account = Account("DUMMY_ACCOUNT")
    portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"GOOG": 0.5, "PINS": 0.5})
    account.set_strategy(portfolio_rebalance_strategy)
    account.add_cash(10000)

    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2020, 2, 1)
    day_range = (end_date - start_date).days
    for day in range(day_range):
        date = start_date + timedelta(days=day)
        market.set_date(date)
        account.trade()
        account.show()

if __name__ == "__main__":
    main()