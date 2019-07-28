class MockMetric:
    def __init__(self, services):
        self.influxdb = services['InfluxDBService'].influxdb

    def run(self):
        points = [
            {
                'measurement': 'weather.temperature',
                'tags': {
                    'location': 'Zurich',
                },
                'fields': {
                    'celsius': 37.5
                }
            }
        ]
        self.influxdb.write_points(points)
