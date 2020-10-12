from flywheel.signals.signals_class.signal_factory import signal_factory

if __name__ == '__main__':
    factory = signal_factory()
    volume_signal = factory.get_signal('volume')
    dates = ['2020-09-10', '2020-09-11', '2020-09-12']
    volumes = volume_signal.get_multidate_value('GOOG', dates)
    print(volumes)