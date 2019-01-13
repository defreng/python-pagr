import os

from pagr.mbook import MBook


def test_config1():
    config_path = os.path.join(os.getcwd(), 'resources', 'config1.yaml')

    mbook = MBook(config_path)
    assert len(mbook.metrics) == 1

    mbook.run()

    metric = mbook.metrics[0][1]
    assert len(metric.influxdb.method_calls) == 1


def test_config_import():
    config_path = os.path.join(os.getcwd(), 'resources', 'config1_import.yaml')

    mbook = MBook(config_path)
    assert len(mbook.metrics) == 2
    assert mbook.services['influxdb']
