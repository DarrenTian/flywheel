import numpy as np
import pandas as pd

def price_to_returns(prices):
    return prices.pct_change().fillna(0)

def max_drawdown(prices):
    return (prices / prices.expanding(min_periods=0).max()).min() - 1

def drawdowns(prices):
    drawdown_series = prices / prices.expanding(min_periods=0).max() - 1
    print(drawdown_series)
    # drawdown series is either 0 or negative
    in_drawdown = drawdown_series < 0
    # extract drawdown start dates
    starts = (~in_drawdown).shift(1) & in_drawdown
    starts = list(starts[starts].index)
    # extract drawdown end dates
    ends = (~in_drawdown).shift(-1) & in_drawdown
    ends = list(ends[ends].index)
    # theoretically series won't start in drawdown
    # when series end in drawdown, add last date
    if ends and starts[-1] > ends[-1]:
        ends.append(drawdown_series.index[-1])
    drawdowns_summary = []
    for drawdown_index, _ in enumerate(starts):
        start = starts[drawdown_index]
        end = ends[drawdown_index]
        drawdown = drawdown_series[start:end+1]    
        print(drawdown)
        drawdowns_summary.append((start, drawdown.idxmin(), end, end-start+1))
    df = pd.DataFrame(data=drawdowns_summary,
                      columns=('start', 'valley', 'end', 'days'))
    return df

def longest_drawdown_days(prices):
    return drawdowns(prices)['days'].max()
    
def total_return(returns):
    return returns.sum()

def sharp(returns, rf_rate, days = 252):
    volatility = returns.std() * np.sqrt(days)
    sharpe_ratio = (returns.mean() - rf_rate) / volatility
    return sharpe_ratio

def calculate_metrics(prices):
    metrics = {}

    returns = price_to_returns(prices)
    metrics['Total Return'] = total_return(returns)
    metrics['Max DrawDown'] = max_drawdown(prices)
    # metrics['Longest DrawDown Days'] = longest_drawdown_days(prices)
    metrics['Sharp Ratio'] = sharp(returns, rf_rate = 0.)
    # TODO: 
    #   Exposure
    #   CAGR
    #   Sortino
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


