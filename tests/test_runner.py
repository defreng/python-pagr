from unittest.mock import patch

from pagr.runner import run_folder


@patch.dict('os.environ', {
    'PAGR_INFLUXDB_HOST': 'myhost',
})
def test_run_folder_mock():
    objects = run_folder(['resources/test_run_folder_mock'])

    assert len(objects) == 3
    assert 'MockMetric' in objects[2]
    assert 'Mock2Metric' in objects[2]
    assert 'SubfolderMetric' in objects[2]
    assert objects[2]['SubfolderMetric']['instance'].ran

    assert len(objects[1]['InfluxDBService'].influxdb.method_calls) == 2
    assert objects[1]['InfluxDBService'].configuration['INFLUXDB_HOST'] == 'myhost'


@patch.dict('os.environ', {
    'PAGR_INFLUXDB_HOST': 'myhost',
})
def test_run_folder_mock_metric_selection():
    objects = run_folder(['resources/test_run_folder_mock', '-m', 'MockMetric'])

    assert len(objects[2]) == 1


@patch.dict('os.environ', {
    'PAGR_INFLUXDB_HOST': 'myhost',
    'PAGR_METRICS': 'MockMetric'
})
def test_run_folder_mock_metric_selection_env():
    objects = run_folder(['resources/test_run_folder_mock'])

    assert len(objects[2]) == 1


@patch.dict('os.environ', {
    'PAGR_INFLUXDB_HOST': 'myhost',
})
def test_run_folder_mock_metric_multi_selection():
    objects = run_folder(['resources/test_run_folder_mock', '-m', 'MockMetric', '-m', 'Mock2Metric'])

    assert len(objects[2]) == 2


@patch.dict('os.environ', {
    'PAGR_INFLUXDB_HOST': 'myhost',
    'PAGR_METRICS': 'MockMetric,SubfolderMetric'
})
def test_run_folder_mock_metric_multi_selection_env():
    objects = run_folder(['resources/test_run_folder_mock'])

    assert len(objects[2]) == 2


def test_run_folder_empty():
    objects = run_folder(['resources/test_run_folder_empty'])

    assert len(objects[1]) == 0
    assert len(objects[2]) == 0

