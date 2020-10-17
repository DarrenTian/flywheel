import flywheel.proto_gen.signal.signal_pb2 as Signal

from datetime import date
from flywheel.signals.signals_class.signal_factory import signal_factory

# Output signals for one ticket_name
def get_signals(ticket_name):
    meta_signal = Signal.MetaSignal()
    meta_signal.ticket_name = ticket_name

    factory = signal_factory()
    price_signal = factory.get_signal('price')
    today_date = str(date.today())[:10]
    ema = price_signal.get_ema('GOOG', today_date, 200)
    meta_signal.base_signal.price_signal = ema

if __name__ == '__main__':
    get_signals('GOOG')