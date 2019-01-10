import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from simpleatlassian.bitbucket import BitBucket


class BitbucketService:
    def __init__(self, configuration):
        self._api_base_url = configuration['BITBUCKET_API_BASE_URL']
        self._host = configuration.get('BITBUCKET_HOST', None)
        self._username = configuration.get('BITBUCKET_USERNAME', None)
        self._password = configuration.get('BITBUCKET_PASSWORD', None)
        self._ssl_verify = bool(configuration.get('BITBUCKET_SSL_VERIFY', True))

        extra_headers = None
        if self._host is not None:
            extra_headers = {
                'Host': self._host
            }
        self.bitbucket = BitBucket(self._api_base_url,
                                   username=self._username,
                                   password=self._password,
                                   extra_headers=extra_headers,
                                   verify=self._ssl_verify
                                   )
