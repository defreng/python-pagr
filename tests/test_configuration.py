from unittest.mock import patch

from pagr.configuration import ConfigurationProvider


@patch.dict('os.environ', {'PAGR_TEST_CONFIG_1': 'blabla'})
def test_configuration_load():
    conf = ConfigurationProvider()

    assert conf['TEST_CONFIG_1'] == 'blabla'
