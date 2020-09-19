from flywheel.signals.factor.factor_factory import factor_factory

if __name__ == '__main__':
    factory = factor_factory()
    volume_factor = factory.get_factor('volume')
    dates = ['2020-09-10', '2020-09-11', '2020-09-12']
    volumes = volume_factor.get_multidate_value('GOOG', dates)
    print(volumes)