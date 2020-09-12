import abc

from flywheel.market.db import db


# A factory to generate factor class.
# Please add [factor_name, factor_class] in the factor_list when you implement a new factor.
# E.g.
# factory = factor_factory()
# volume_factor = factory.get_factor('volume')
class factor_factory:

    def __init__(self):
        self.db = db()
        self.factor_list = {}

    def get_factor(self, factor_name):
        if factor_name in self.factor_list:
            factor_instance = self.factor_list[factor_name]
            factor_instance.set_database(self.db)
            return factor_instance
        else:
            raise ValueError('Cannot find this factor. Please use the correct factor name or create a type of factor class')


class factor(metaclass=abc.ABCMeta):

    def __init__(self, factor_name):
        self.name = factor_name

    def set_database(self, db):
        self.db = db