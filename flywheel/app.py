from flywheel import flags
from flywheel.service.google import GoogleService

def run():
  # TODO: Get up-to-date market data
  # TODO: Generate signals based on market data
  # TODO: Translate signals into Buy/Sell decisions
  # TODO: Strategize Buy/Sell decisions
  # TODO: Evaluate past performanace
  content = "Hello World"
  if flags.flags().email:
    GoogleService().send_mail(content)