import os

from pagr.runner import run_folder


def test_run_folder_mock():
    os.environ['PAGR_INFLUXDB_HOST'] = 'myhost'

    objects = run_folder(['resources/test_run_folder_mock'])

    assert len(objects) == 1
    assert len(objects[0][1]['InfluxDBService'].influxdb.method_calls) == 1
    assert objects[0][1]['InfluxDBService'].configuration['INFLUXDB_HOST'] == 'myhost'


def test_run_folder_empty():
    objects = run_folder(['resources/test_run_folder_empty'])

    assert len(objects) == 1
    assert len(objects[0][1]) == 0
    assert len(objects[0][2]) == 0


def test_internal_services_available():
    os.environ['PAGR_INFLUXDB_HOST'] = 'myhost'

    objects = run_folder(['resources/test_run_folder_empty'])

    assert len(objects) == 1

    test_service = objects[0][1]['TestService']
    test_service.a = 1234

    test_service2 = objects[0][1]['TestService']
    assert test_service2.a == 1234

    assert objects[0][1]['TestService'].configuration['INFLUXDB_HOST'] == 'myhost'

