from flywheel.signals.signals_class.signal_factory import signal_factory


def test():
    factory = signal_factory()
    volume_signal = factory.get_signal('volume')
    dates = ['2020-09-10', '2020-09-11', '2020-09-12']
    volumes = volume_signal.get_multidate_value('GOOG', dates)
    print(volumes)

def test_rsi():
    factory = signal_factory()
    price_signal = factory.get_signal('price')
    date = '2020-09-14'
    rsi = price_signal.rsi('GOOG', date)
    print(rsi)

if __name__ == '__main__':
    test_rsi()