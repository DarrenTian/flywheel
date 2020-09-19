import abc

class factor(metaclass=abc.ABCMeta):

    def __init__(self, factor_name):
        self.name = factor_name

    def set_database(self, db):
        self.db = db