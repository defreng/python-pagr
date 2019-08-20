class SubfolderMetric:
    def __init__(self, services):
        self.influxdb = services['InfluxDBService'].influxdb
        self.ran = False

    def run(self):
        self.ran = True
