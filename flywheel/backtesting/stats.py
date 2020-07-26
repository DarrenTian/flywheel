def returns(prices):
    return prices.pct_change().fillna(0)

def max_drawdown(prices):
    return (prices / prices.expanding(min_periods=0).max()).min() - 1

def total_return(returns):
    return returns.sum()

