from flywheel.market.db import db
from flywheel.signals.signals_class.signal_list import signal_list

# A signal to generate signals_class class.
# Please add [signal_name, signal_class] in the factor_list when you implement a new signals_class.
# E.g.
# factory = signal_factory()
# volume_signal = factory.get_signal('volume')
# dates = ['2020-09-01', '2020-09-02', '2020-09-03']
# volumes = volume_signal.get_multidate_value('GOOG', dates)

class signal_factory:

    def __init__(self):
        self.db = db()
        self.signal_list = signal_list

    def get_signal(self, signal_name):
        if signal_name in self.signal_list:
            signal_instance = self.signal_list[signal_name](signal_name)
            signal_instance.set_database(self.db)
            return signal_instance
        else:
            raise ValueError('Cannot find this signals_class. Please use the correct signals_class name or create a type of signals_class class')
