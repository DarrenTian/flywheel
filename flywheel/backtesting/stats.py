import numpy as np

def returns(prices):
    return prices.pct_change().fillna(0)

def max_drawdown(prices):
    return (prices / prices.expanding(min_periods=0).max()).min() - 1

def total_return(returns):
    return returns.sum()

def sharp(returns, rf_rate, days = 252):
    volatility = returns.std() * np.sqrt(days)
    sharpe_ratio = (returns.mean() - rf_rate) / volatility
    return sharpe_ratio

def calculate_metrics(prices):
    metrics = {}

    returns = prices.pct_change().fillna(0)
    metrics['Total Return'] = total_return(returns)
    metrics['Max DrawDown'] = max_drawdown(prices)
    metrics['Sharp Ratio'] = sharp(returns, rf_rate = 0.)
    # TODO: 
    #   Exposure
    #   CAGR
    #   Sharp Ratio
    #   Sortino
    #   Longest DD Days
    #   Risk-free rate
    #   Volatility
    #   Annual Volatitiy
    #   R2
    #   Calmar
    #   Skew
    #   Kurtosis
    #   Expected Daily/Monthly/Yearly Return
    #   Kelly Criterion
    #   Risk of Ruin
    #   Daily Value-at-Risk
    #   Expected Shortfall(cVaR)
    #   Payoff Ratio
    #   Profit Factor
    #   Common Sense Ratio
    #   CPC Index
    #   Tail Ratio
    #   Outlier Win Ratio
    #   Outlier Loss Ratio
    #   MTD
    #   3M/6M/YTD/1Y/3Y(anl)/5Y(anl)/10Y(anl)/all-time(anl)
    #   Best/Worst Day/Month/Year
    #   Avg drawdown
    #   Avg drawdown days
    #   Win days/month/quarter/year %
    #   Beta/Alpha
    #   EoY return by year, vs. benchmark
    #   Worst 10 drawdowns

    return metrics


