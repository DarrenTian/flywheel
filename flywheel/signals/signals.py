import json
import matplotlib.pyplot as plt
import os
import sys

from datetime import date

DUMMY_DATA_PATH_WINDOWS = "C:\\Users\\silentsea\\Desktop\\projects\\flywheel\\flywheel\\market\\stock_data.json"
DUMMY_DATA_PATH = "../market/stock_data.json"
MOD_CANDIDATES = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]

def get_price():
    with open(DUMMY_DATA_PATH, 'r') as json_file:
        stock_data = json.load(json_file)
        return stock_data

def process_market_data(market_data):
    flag = True
    for ticker in market_data:
        ema = get_ema(market_data[ticker], "Close")
        print(ema)
        if flag:
            lineplot(ema.keys(), ema.values())
            flag = False

# return dict{zip(date, ema)}        
def get_ema(stock_data, mod):
    ema = {}
    N = 0
    ema_t0 = 0
    plt.figure()
    for date in stock_data:
        stock_data_daily = stock_data[date]
        N += 1
        alpha = 2.0 / (N + 1)
        ema_t1 = ema_t0 + alpha * (stock_data_daily[mod] - ema_t0)
        ema[date] = ema_t1
        ema_t0 = ema_t1
    return ema

# return dict{zip(date, ema_dif)}
def get_ema_dif(ema_dict, day_range_alpha, day_range_beta):
    ema_tuples = ema_dict.items()
    ema_dif = {}
    if (len(ema_tuples) < day_range_beta):
        return ema_dif
    ema_slow = 0
    ema_fast = 0
    slow_head = 0
    fast_head = 0
    N_slow = 0
    N_fast = 0
    for i in range(len(ema_tuples)):
        N_fast += 1
        N_slow += 1
        date, ema = ema_tuples[i]
        ema_dif[date] = 0
        if (N_fast >= day_range_alpha):
            N_fast = day_range_alpha
            ema_fast = culmulative_range_average(ema_fast, N_fast, ema, ema_tuples[fast_head][1])
            fast_head += 1
        else:
            ema_fast = culmulative_range_average(ema_fast, N_fast, ema, 0)
        if (N_slow >= day_range_beta):
            N_slow = day_range_beta
            ema_slow = culmulative_range_average(ema_slow, N_slow, ema, ema_tuples[slow_head][1])
            slow_head += 1
            ema_dif[date] = ema_fast - ema_slow
        else:
            ema_slow = culmulative_range_average(ema_slow, N_slow, ema, 0)
    return ema_dif

def get_macd(ema_dif, day_range):
    macd = {}
    ema_tuples = ema_dif.items()
    if (len(ema_tuples) < day_range):
        return macd
    N = 0
    head = 0
    ema_culmulative = 0
    for i in range(len(ema_tuples)):
        N += 1
        date, ema = ema_tuples[i]
        if (N >= day_range):
            N = day_range
            ema_culmulative = culmulative_range_average(ema_culmulative, N, ema, ema_tuples[head][1])
            head += 1
            macd[date] = ema_culmulative
        else:
            ema_culmulative = culmulative_range_average(ema_culmulative, N, ema, 0)
    return macd    

def culmulative_range_average(pre_average, N, new_value, old_value):
    return pre_average + (new_value - old_value) / N

def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

def testplot():
    plt.subplots(1, 1)
    x= range(100)
    y= [i**2 for i in x]

    plt.plot(x, y, linewidth = '1', label = "test", color='#539caf', linestyle=':', marker='|')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    #print(sys.path)
    #print(os.getcwd())
    #print(get_price("msft"))
    market_data = get_price()
    process_market_data(market_data)
    #testplot()