from flywheel import market
import copy

SHOW_ALLOCATION = False

# class Portfolio:
#   """docstring for ClassName"""
#   def __init__(self, name):
#     self.parent = None
#     self.name = name
#     self.portfolios = []
#     self.portfolio_dist = {}
#     # self.instruments = []
#     # self.instrument_dist = {}
#     self.status = 'ACTIVE'
#     self.allocation = 0

#   def get_equity(self):
#     instruments = self.get_instruments()
#     return sum([instruments[ins].get_equity() for ins in instruments])

#   def get_root(self):
#     if self.parent == None:
#       return self
#     else:
#       return self.parent.get_root()

#   def path(self):
#     if self.parent == None:
#       return "/"
#     return "{} > {}".format(self.parent.path(), self.name)

#   def get_portfolio_by_name(self, name):
#     if self.name == name:
#       return self
#     found_portfolio = None
#     for portfolio in self.portfolios:
#       found_portfolio = portfolio.get_portfolio_by_name(name)
#       if found_portfolio != None:
#         return found_portfolio

#   def get_instruments(self):
#     instruments = {}
#     self.get_instruments_internal(instruments)
#     return instruments

#   def get_instruments_internal(self, instruments):
#     if isinstance(self, Instrument):
#       if self.name not in instruments:
#         instruments[self.name] = copy.copy(self)
#       else:
#         instruments[self.name].union(self)
#       #print "Adding {} with {} and {}".format(self.name, instruments[self.name].allocation, instruments[self.name].liability)
#       return
#     else:
#       for portfolio in self.portfolios:
#         portfolio.get_instruments_internal(instruments)

#   def add_amount(self, amount):
#     self.allocation += amount
#     self.update_status()
#     if self.parent != None:
#       self.parent.add_amount(amount)

#   def remove_amount(self, amount):
#     self.allocation -= amount
#     if self.parent != None:
#       self.parent.remove_amount(amount)

#   def update_status(self):
#     has_active = False
#     for portfolio in self.portfolios:
#       if portfolio.status == 'ACTIVE':
#         has_active = True
#         break
#     if not has_active:
#       self.status = 'RESERVED'
#     return

#   def allocation_type(self):
#     active_portfolios = filter(lambda portfolio:portfolio.status=='ACTIVE', self.portfolios)
#     active_count = len(active_portfolios)
#     has_dist = bool(self.portfolio_dist)
#     active_portfolios_in_dist = set([portfolio.name for portfolio in active_portfolios])==set(self.portfolio_dist.keys())
#     # LEAF
#     if active_count == 0 and not has_dist:
#       return 'LEAF'
#     # First Kind: Only one active, no dist
#     if active_count == 1 and not has_dist:
#       return 'ONE_ACTIVE'
#     # print active_count, has_dist
#     if active_count > 1 and has_dist:
#       if not active_portfolios_in_dist:
#         print("Can not found active portfolio in dist")
#         return
#       sum_dist = sum(self.portfolio_dist.values())
#       if (1-sum_dist) > 0.0001:
#         print("Distribution doesn't add up to 1.0")
#       return 'DIST'
#     else:
#       print("Something is wrong, can not figure out how to allocate")
  
#   def allocate_one_active(self, amount):
#     if SHOW_ALLOCATION:
#        print("Allocating ONE_ACTIVE {} with {}".format(self.name, amount))

#     active_portfolio = None
#     for portfolio in self.portfolios:
#       if portfolio.status == 'ACTIVE':
#         active_portfolio = portfolio
#     active_portfolio.allocate(amount)

#   def allocate_dist(self, amount):
#     if SHOW_ALLOCATION:
#       print("Allocate DIST {} with {}".format(self.name, amount))
#     absolute_value = amount+self.allocation
#     portfolio_allocation = {}
#     for portfolio in self.portfolios:
#       portfolio_allocation[portfolio.name] = portfolio.allocation
#     for portfolio in self.portfolios:
#       if portfolio.status == 'ACTIVE':
#         to_be_allocated = absolute_value*self.portfolio_dist[portfolio.name] - portfolio_allocation[portfolio.name]
#         if to_be_allocated < 0:
#           print("No enough fund to be allocated, {}:{} is less than {}".format(portfolio.name, self.portfolio_dist[portfolio.name], portfolio_allocation[portfolio.name]/self.allocation))
#           return
#         portfolio.allocate(to_be_allocated)

#   def allocate(self, amount):
#     if SHOW_ALLOCATION:
#       print("Allocate {} with {}".format(self.name, amount))
#     if self.status != 'ACTIVE':
#       print("The portfolio is not allocatable")

#     allocation_type = self.allocation_type()
#     # print allocation_type
#     if allocation_type == 'LEAF':
#       self.reserve_allocation(amount)
#     if allocation_type == 'ONE_ACTIVE':
#       self.allocate_one_active(amount)
#     if allocation_type == 'DIST':
#       self.allocate_dist(amount)

#   def has_active_portfolio(self):
#     for portfolio in self.portfolios:
#       # print portfolio.name, portfolio.type
#       if portfolio.type == 'ACTIVE':
#         return True
#     return False

#   def has_eligible_portfolios(self):
#     has_dist_portfolio = False
#     has_non_dist_portfolio = False
#     for portfolio in self.portfolios:
#       if portfolio.name in self.portfolio_dist.keys():
#         has_dist_portfolio = True
#       else:
#         has_non_dist_portfolio = True
#     if has_dist_portfolio and has_non_dist_portfolio:
#       return False
#     return True

#   def add_portfolio(self, portfolio):
#     self.portfolios.append(portfolio)
#     portfolio.parent = self

#   def add_portfolio_by_dist(self, portfolio, dist):
#     self.portfolios.append(portfolio)
#     portfolio.parent = self
#     self.portfolio_dist[portfolio.name] = dist

#   def remove_portfolio(self, portfolio):
#     self.portfolios.remove(portfolio)

#   def show(self):    
#     return self.show_internal("-")

#   def show_internal(self, prefix):
#     if SHOW_ALLOCATION:
#       content = "{}({})portfolio for {}:{:.2f}\n".format(prefix, self.status, self.path(), float(self.get_equity())) 
#     else:
#       content = "{} {}:{:.2f}\n".format(prefix, self.path(), float(self.get_equity()))
#     for portfolio in self.portfolios:
#       content += portfolio.show_internal("-{}".format(prefix))
#     return content

# class Account(Portfolio):
#   def __init__(self, name, managed_cash):
#     Portfolio.__init__(self, name)
#     self.managed_cash = managed_cash

#   def get_net_asset(self):
#     return self.get_equity()

#   def get_liability(self):
#     instruments=self.get_instruments()
#     liability = sum([ins.liability for ins in instruments.values()])
#     return liability

#   def get_asset(self):
#     return self.get_net_asset() - self.get_liability()

#   def get_retire_asset(self):
#     return self.get_portfolio_by_name('Retirement').get_equity()

#   def get_cash(self):
#     return self.managed_cash.get_equity()

#   def get_rsu(self):
#     instruments=self.get_instruments()
#     return sum([instruments[ins].get_equity() for ins in instruments and STOCK_ASSET])

#   def get_crypto(self):
#     return self.get_portfolio_by_name('BTC-USD').get_equity()

#   def get_gold(self):
#     return self.get_portfolio_by_name('IAU').get_equity()

#   def liquidate(self, portfolio):
#     # sell self
#     liquidated_amount = portfolio.get_equity()
#     portfolio.parent.remove_portfolio(portfolio)
#     self.managed_cash.add_equity(liquidated_amount)

#   def purchase(self, parent_instrument, instrument, asset, debt=0):
#     managed_cash = self.managed_cash
#     equity = asset + debt
#     if managed_cash.allocation < equity:
#       print("No way you can buy {} worth {} with cash {}!".format(instrument.name, equity, managed_cash.get_equity()))
#       return
#     managed_cash.remove_equity(equity)
#     parent_instrument.add_portfolio(instrument)
#     instrument.add_equity(asset+debt, debt)

class Instrument:
  def __init__(self, name):
    self.name = name
    self.position = 0

  # def get_equity(self):
  #   if self.equity > 0:
  #     return self.equity
  #   if self.position > 0:
  #     return self.position * market.get_price(self.name) + self.liability
  #   return 0

  # def union(self, instrument):
  #   self.equity += instrument.equity
  #   self.allocation += instrument.allocation
  #   self.liability += instrument.liability

  # def reserve_allocation(self, amount):
  #   self.equity = amount

  #   # Allocation related
  #   self.status = 'RESERVED'
  #   self.allocation = amount
  #   self.parent.add_amount(amount)
  #   if SHOW_ALLOCATION:
  #     print("Reserving {} with {}".format(self.name, amount))

  # def reserve_allocation_with_debt(self, amount, liability):
  #   if SHOW_ALLOCATION:
  #     print("Reserving {} with {} and debt {}".format(self.name, amount, liability))
  #   self.status = 'RESERVED'
  #   self.equity = amount + liability
  #   self.liability = liability
  #   self.add_amount(amount+liability)
  #   # Deal with children
  #   # TODO
  #   # Reflect in parent
  #   self.parent.update_status()

  # def reserve_position(self, position):
  #   self.position = position

  #   # Allocation related
  #   self.status = 'RESERVED'
  #   self.allocation = self.get_equity()
  #   self.parent.add_amount(self.get_equity())
  #   if SHOW_ALLOCATION:
  #     print("Reserving {} with {}".format(self.name, self.get_equity()))


  # def reserve_position_with_debt(self, position, liability):
  #   self.liability = liability
  #   self.reserve_position(position)
