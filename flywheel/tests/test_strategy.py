from flywheel.strategy.portfolio import Instrument

def test(): 
    pins_portfolio = Instrument('PINS')
    print(pins_portfolio.name)
    # goog_portfolio = Instrument('GOOG')
    # managed_cash_portfolio = Instrument('CASH')
    # managed_portfolio = Portfolio('MANAGED')
    # managed_portfolio.add_portfolio(pins_portfolio)
    # managed_portfolio.add_portfolio(goog_portfolio)
    # managed_portfolio.add_portfolio(managed_cash_portfolio)

if __name__ == "__main__":
    test()