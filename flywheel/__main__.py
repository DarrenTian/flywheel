import click 

from flywheel.utils.google import GoogleService
from flywheel.settings import STOCK_LIST
from flywheel.signals import signals
from flywheel.market import market

@click.command()
@click.option('--email', default=False, help='if set, will trigger email')
@click.option('--debug', default=False, help='if set, will enable debug information')
def cli(email, debug):   
    # Putting into separate loops so they can be decoupled later
    for ticker in STOCK_LIST:
        market.update(ticker)

    # Get stock data
    # Generate signals
    for ticker in STOCK_LIST:
        signals.compute(ticker)

    email_content = ""
    for ticker in STOCK_LIST:
        recommendation = signals.recommend(ticker)
        email_content += "{} : {}\n".format(ticker, recommendation)     

    # Based on threshold from backtesting, decide buy/sell signal
    # Send email
    if email:
        GoogleService().send_mail('')

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter