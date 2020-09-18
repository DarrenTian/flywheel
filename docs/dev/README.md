# Dev Doc

This doc dir is for the developer.

## Software Dependency

| Software | Version |
|----------|---------|
| python   | 3.7     |
| mysql    | 5.7     |
| redis    | 5.0     |

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
├── models.py # orm models
├── settings.py # configs
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
$ pipenv run python -m flywheel
$ pipenv run python -m flywheel --email # send email
```

### run individual script
If you are trying to hack up test by implementing main function in individual script:
```commandline
$ pipenv run python -m flywheel.signals.signals
```
This can help resolve any relative path issue.

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

## Cron tasks

This project use [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) to implement async job and cron job, all the task was defined in the tasks package:

```commandline
$ tree tasks
tasks
├── __init__.py # all the celery tasks can be found in it
└── cron.py # all the celery cron tasks can be found in it
```

## Deploy

First the remote server should have `docker` and `docker-compose` installed.

### rsync way 

You can deploy this project to remote server by `rsync`:

```commandline
$ rsync -r -v --exclude-from=./rsync.excludes . $remote_server:/srv/flywheel
$ make build
$ make docker-run
```

### docker way

Also you can deploy this project to remote server by docker way:

1. First you should config the `docker registry` (usually is a private registry) in your local machine and remote server.
2. Build image locally and upload built image to the docker registry. 
3. Upload the docker-compose file `docker-compose.yml` to the remote server working dir.
4. Run this make cmd: `make docker-run` in your working dir.
