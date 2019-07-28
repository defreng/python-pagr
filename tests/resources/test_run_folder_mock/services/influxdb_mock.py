from unittest import mock


class InfluxDBService:
    def __init__(self, configuration):
        self.configuration = configuration
        self.influxdb = mock.Mock()
