import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from simpleatlassian import JIRA


class JiraService:
    def __init__(self, configuration):
        self._api_base_url = configuration['JIRA_API_BASE_URL']
        self._host = configuration.get('JIRA_HOST', None)
        self._username = configuration.get('JIRA_USERNAME', None)
        self._password = configuration.get('JIRA_PASSWORD', None)
        self._ssl_verify = bool(configuration.get('JIRA_SSL_VERIFY', True))

        extra_headers = None
        if self._host is not None:
            extra_headers = {
                'Host': self._host
            }
        self.jira = JIRA(self._api_base_url,
                         username=self._username,
                         password=self._password,
                         extra_headers=extra_headers,
                         verify=self._ssl_verify)
