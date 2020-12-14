import flywheel.proto_gen.signal.signal_pb2 as Signal

from datetime import date
from flywheel.signals.signals_class.signal_factory import signal_factory

# Output signals for one ticket_name
def get_signals(ticket_name):
    meta_signal = Signal.MetaSignal()
    meta_signal.ticket_name = ticket_name

    factory = signal_factory()
    today_date = str(date.today())[:10]

    # get ema
    price_signal = factory.get_signal('price')
    ema = price_signal.ema(ticket_name, today_date, 200)
    meta_signal.base_signal.price_signal.price_ema_200.date = today_date
    meta_signal.base_signal.price_signal.price_ema_200.value = ema

    # get rsi
    rsi = price_signal.rsi(ticket_name, today_date)
    meta_signal.base_signal.price_signal.price_rsi.date = today_date
    meta_signal.base_signal.price_signal.price_rsi.value = rsi

    # get volume
    volume_signal = factory.get_signal('volume')
    meta_signal.base_signal.volume_signal.volume.raw_volume = volume_signal.get_value(ticket_name, today_date)


if __name__ == '__main__':
    get_signals('GOOG')