import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from influxdb import InfluxDBClient


class InfluxDBService:
    def __init__(self, configuration):
        self._database_name = configuration['INFLUXDB_DBNAME']
        self._host = configuration.get('INFLUXDB_HOST', 'localhost')
        self._port = configuration.get('INFLUXDB_PORT', 8086)
        self._username = configuration.get('INFLUXDB_USERNAME', None)
        self._password = configuration.get('INFLUXDB_PASSWORD', None)
        self._path = configuration.get('INFLUXDB_PATH', '/')
        self._ssl = configuration.get('INFLUXDB_SSL_ENABLED', False)

        self.influxdb = InfluxDBClient(self._host, self._port, self._username, self._password,
                                       self._database_name, path=self._path, ssl=self._ssl)
