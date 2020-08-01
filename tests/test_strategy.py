from flywheel.market.market import Market
from flywheel.strategy.account import Account
from flywheel.strategy.strategy import DoNothingStrategy, PortfolioRebalanceStrategy


def test_do_nothing_strategy():
    account = Account("DUMMY_ACCOUNT")
    account.add_cash(10000)
    market = Market()
    account.set_market(market)
    do_nothing_strategy = DoNothingStrategy()
    account.set_strategy(do_nothing_strategy)
    account.trade()
    account.show()


def test_portfolio_rebalance_strategy():
    account = Account("DUMMY_ACCOUNT")
    account.add_cash(10000)
    market = Market()
    account.set_market(market)
    portfolio_rebalance_strategy = PortfolioRebalanceStrategy({"GOOG": 0.5, "PINS": 0.5})
    account.set_strategy(portfolio_rebalance_strategy)
    account.trade()
    account.show()
