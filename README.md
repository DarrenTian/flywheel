# flywheel

flywheel is a personal investment recommendation tool, until we make it a sophisticated trading bot. :)

## Components
app: where the main app runs

app>market: where we get market data

app>signals: where we derive signals from market data

app>strategy: where we decide investment strategy

## Build & Run
pipenv install

pipenv shell

python -m flywheel

(Send email): python flywheel --email

## TESTS
python -m flywheel.tests.test_{test_name}
