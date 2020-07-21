from collections import defaultdict
from flywheel.market import market

class Account:
  def __init__(self, name):
    self.name = name
    self.cash = 0
    self.holdings = defaultdict(int)
    self.strategy = None
  
  def add_cash(self, amount):
    self.cash += amount
  
  def set_strategy(self, strategy):
    self.strategy = strategy
  
  # If without specific date, we get operate on the latest market data.
  def trade(self):
    operations = self.strategy.get_operations(self.cash, self.holdings)
    for operation in operations:
      self.operate(operation)
  
  def operate(self, operation):
    if operation.type == 'SELL':
      self.liquidate(operation.ticker, operation.position)
    if operation.type == 'BUY':
      self.purchase(operation.ticker, operation.position)

  def liquidate(self, ticker, position):
    self.holdings[ticker] -= position
    self.cash += market.get_price(ticker) * position
  
  def purchase(self, ticker, position):
    self.cash -= market.get_price(ticker) * position
    self.holdings[ticker] += position
  
  def show(self):
    print("Cash: {}".format(self.cash))
    for holding in self.holdings:
      print("{}: {}".format(holding, self.holdings[holding]))