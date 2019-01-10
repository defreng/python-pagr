import jenkins


class JenkinsService:
    def __init__(self, configuration):
        self._base_url = configuration['JENKINS_BASE_URL']
        self._username = configuration.get('JENKINS_USERNAME', None)
        self._password = configuration.get('JENKINS_PASSWORD', None)

        self.jenkins = jenkins.Jenkins(self._base_url, username=self._username, password=self._password)
        self.jenkins._session.auth = (self._username, self._password)
