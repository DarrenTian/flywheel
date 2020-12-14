import abc

class signal(metaclass=abc.ABCMeta):

    def __init__(self, signal_name):
        self.name = signal_name

    def set_database(self, db):
        self.db = db