# General Util Function/Api
import pandas as pd
import pandas_market_calendars as mcal

# get N vaild market dates
def valid_market_dates(end_date, N):
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date='2010-01-01', end_date=end_date)
    dates = early.index[-N:]
    dates = [str(date)[:10] for date in dates]
    return dates
