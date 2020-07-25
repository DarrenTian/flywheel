# flywheel

flywheel is a personal investment recommendation tool, until we make it a sophisticated trading bot. :)

## Project Structure

```commandline
$ tree . # mac: brew install tree, this tool will print everything in the folder.
.
├── Dockerfile # docker build file
├── Makefile # where you can define some cmd collection in it
├── Pipfile # pipenv config file
├── Pipfile.lock # pipenv lock file
├── README.md # doc
├── docker-compose.yml # docker-compose config file
├── docs # where you can write project doc in it
├── flywheel # project main package
├── production
├── scripts # where you can write some migrate scripts in it
├── tasks # celery tasks
└── tests # tests package
```

## Components

```commandline
$ tree flywheel # mac: brew install tree, this tool will print everything in the folder.
flywheel
├── __init__.py
├── __main__.py
├── backtesting
│   ├── __init__.py
│   └── backtesting.py
├── cli.py # command line tool
├── exceptions.py
├── market # where we get market data
│   ├── __init__.py
│   ├── factor.py
│   ├── market.py
│   ├── stock_data.json
│   ├── stock_list
│   └── yahoo.py
├── models.py
├── settings.py
├── signals # where we derive signals from market data
│   ├── README.txt
│   ├── TODO
│   └── __init__.py
├── strategy # where we decide investment strategy
│   ├── __init__.py
│   ├── account.py
│   └── strategy.py
└── utils
    ├── __init__.py
    ├── config.py
    └── google.py
```

## Build & Run

### dev run

```commandline
$ pipenv install
$ pipenv run python -m flywheel.cli
$ pipenv run python -m flywheel.cli --email # send email
```

### docker run

```commandline
$ make build
$ make docker-run
```

First run, you should init db by:

```commandline
$ pipenv run python scripts/db.py
```

## TESTS

```commandline
$ pipenv run pytest tests
```
