import json
import matplotlib.pyplot as plt
import os
import sys

from datetime import date

DUMMY_DATA_PATH_WINDOWS = 'C:\\Users\\silentsea\\Desktop\\projects\\flywheel\\flywheel\\market\\stock_data.json'
DUMMY_DATA_PATH = '../market/stock_data.json'

def get_price():
    with open(DUMMY_DATA_PATH, 'r') as json_file:
        stock_data = json.load(json_file)
        return stock_data

def process_market_data(market_data):
    flag = True
    for ticker in market_data:
        ema = get_ema(market_data[ticker], 'Close')
        print(ema)
        if flag:
            lineplot(ema.keys(), ema.values())
            flag = False

# return zip(date, ema)        
def get_ema(stock_data, mod):
    ema = {}
    N = 0
    ema_t0 = 0
    for date in stock_data:
        stock_data_daily = stock_data[date]
        N += 1
        alpha = 2.0 / (N + 1)
        ema_t1 = ema_t0 + alpha * (stock_data_daily[mod] - ema_t0)
        ema[date] = ema_t1
        ema_t0 = ema_t1
    return ema

def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

if __name__ == '__main__':
    #print(sys.path)
    #print(os.getcwd())
    #print(get_price("msft"))
    market_data = get_price()
    process_market_data(market_data)