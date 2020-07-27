# User Doc

If you want to run locally, you do not need to config anything, 
if you want to run with remote database, 
you should pass a remote connect str env var along with the first cmd when you enter into the python shell, 
for example: `FW_DB_URL=mysql://root:123456@127.0.0.1:3306/flywheel pipenv run ipython`.

## Get Data From Market

### Run in Ipython

```commandline
$ pipenv run ipython
$ from scripts.db import init # init database
$ init()
$ from tasks import crawl_stock_history_data
$ crawl_stock_history_data('GOOG') # crawl the GOOG history data, you can replace GOOG to the stock you need, the default timerange is last one week
```

### Run in Jupyter


## Query Data From Database

### Run in Ipython

```commandline
$ pipenv run ipython
$ from flywheel.handlers import get_stock_prices
$ get_stock_prices('GOOG') # default is return last one week data
```
