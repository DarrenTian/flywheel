import abc

from flywheel.market.db import db


# A factory to generate factor class.
# Please add [factor_name, factor_class] in the factor_list when you implement a new factor.
class factor_factory:

    def __init__(self, factor_name):
        self.db = db()
        self.factor_name = factor_name
        self.factor_list = {}

    def get_factor(self):
        if self.factor_name in self.factor_list:
            factor =  self.factor_list[self.factor_name]
            factor.set_database(self.db)
            return factor
        else:
            raise ValueError('Cannot find this factor. Please use the correct factor name or create a type of factor class')


class factor(metaclass=abc.ABCMeta):

    def __init__(self, factor_name):
        self.name = factor_name

    def set_database(self, db):
        self.db = db