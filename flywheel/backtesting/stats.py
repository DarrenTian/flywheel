import numpy as np
import pandas as pd

from datetime import date, timedelta

def risk_free_rate():
    # TODO: Research how to calculate dynamic risk-free rate
    return 0.

def price_to_returns(prices):
    return prices.pct_change().fillna(0)

def price_to_drawdowns(prices):
    drawdown_series = prices / prices.expanding(min_periods=0).max() - 1
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
    if not ends or (ends and starts[-1] > ends[-1]):
        ends.append(drawdown_series.index[-1])
    drawdowns_summary = []
    for drawdown_index, _ in enumerate(starts):
        start = starts[drawdown_index]
        end = ends[drawdown_index]
        drawdown = drawdown_series[start:end]    
        drawdowns_summary.append((start, drawdown.idxmin(), end, drawdown.count(), drawdown.min())) # We are using trading days
    df = pd.DataFrame(data=drawdowns_summary,
                      columns=('start', 'valley', 'end', 'days', 'max_drawdown'))
    return df

def max_drawdown(drawdowns):
    return drawdowns['max_drawdown'].min()
    # return (prices / prices.expanding(min_periods=0).max()).min() - 1

def longest_drawdown_days(drawdowns):
    return drawdowns['days'].max()

def average_drawdown(drawdowns):
    return drawdowns['max_drawdown'].mean()

def average_drawdown_days(drawdowns):
    return drawdowns['days'].mean()
    
def total_return(returns):
    return returns.add(1).prod() - 1

def returns_to_volatility(returns, annualize = False):
    volatility = returns.std()
    if not annualize:
        return volatility
    else:
        return volatility * np.sqrt(252) # 252 trading days in a year

def sharp(returns, rf_rate):
    volatility = returns_to_volatility(returns, annualize = True)
    sharpe_ratio = (returns.mean() - rf_rate) / volatility
    return sharpe_ratio

# Compound Annual Growth Rate
def cagr(returns):
    years = (returns.index[-1] - returns.index[0]).days / 365.0
    # If shorter than 1 year, return nan
    if years < 1 : return float("nan")
    cagr = total_return(returns) ** (1.0/years) - 1
    return cagr

def calculate_metrics(prices):
    metrics = {}

    returns = price_to_returns(prices)
    metrics['Total Return'] = total_return(returns)
    metrics['Volatility'] = returns_to_volatility(returns, annualize = False)
    metrics['Annual Volatility'] = returns_to_volatility(returns, annualize = True)
    metrics['Sharp Ratio'] = sharp(returns, rf_rate = risk_free_rate())
    # Draw down related metrics
    drawdowns = price_to_drawdowns(prices)
    metrics['Max DrawDown'] = max_drawdown(drawdowns)
    metrics['Longest DrawDown Days'] = longest_drawdown_days(drawdowns)
    metrics['Average DrawDown'] = average_drawdown(drawdowns)
    metrics['Average DrawDown Days'] = average_drawdown_days(drawdowns)
    metrics['Recovery Factor'] = metrics['Total Return'] / abs(metrics['Max DrawDown'])
    # MTD/YTD/3M/6M/1Y/3Y(anl)/5Y(anl)/10Y(anl)/all-time(anl)
    today = date.today()
    metrics['MTD %'] = total_return(returns[returns.index >= date(today.year, today.month, 1)])
    metrics['YTD %'] = total_return(returns[returns.index >= date(today.year, 1, 1)])
    three_months_ago = today - timedelta(days=3*30)
    metrics['3M %'] = total_return(returns[returns.index >= three_months_ago])
    six_months_ago = today - timedelta(days=6*30)
    metrics['6M %'] = total_return(returns[returns.index >= six_months_ago])
    metrics['1Y %'] = total_return(returns[returns.index >= date(today.year - 1, today.month, today.day)])
    metrics['3Y (ann.) %'] = cagr(returns[returns.index >= date(today.year - 3, today.month, today.day)])
    metrics['5Y (ann.) %'] = cagr(returns[returns.index >= date(today.year - 5, today.month, today.day)])
    metrics['10Y (ann.) %'] = cagr(returns[returns.index >= date(today.year - 10, today.month, today.day)])
    metrics['All-time (ann.) %'] = cagr(returns)
    #   Best/Worst Day/Month/Year
    #   Win days/month/quarter/year %
    #   Worst 10 drawdowns
    #   EoY return by year, vs. benchmark
    #  Expected Daily/Monthly/Yearly Return

    # TODO: 
    #   Exposure
    #   Sortino
    #   R2
    #   Calmar
    #   Skew
    #   Kurtosis
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
    #   Beta/Alpha
    return metrics


