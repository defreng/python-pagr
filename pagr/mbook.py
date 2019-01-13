import importlib
import logging
import os
import re

import sys
import yaml


class MBook:
    def __init__(self, yaml_filename):
        self.services = dict()
        self.configuration = dict()
        self.metrics = []

        self._load_configuration(yaml_filename)

    @staticmethod
    def _load_yaml(yaml_filename):
        # add additional resolver to interpret environment variables within the yaml file
        env_matcher = re.compile(r'^\${([^}^{]+)}$')

        def env_constructor(loader, node):
            match = env_matcher.match(node.value)
            return os.environ.get(match.group(1))

        yaml.add_implicit_resolver('!env', env_matcher)
        yaml.add_constructor('!env', env_constructor)
        with open(yaml_filename) as f:
            return yaml.load(f)

    def _load_configuration(self, yaml_filename):
        # add the configuration directory to sys.path, such that we can load metrics/services from there
        basedir = os.path.dirname(yaml_filename)
        sys.path.append(basedir)

        mbook_config = self._load_yaml(yaml_filename)

        for imp in mbook_config.get('imports', []):
            self._load_configuration(os.path.join(basedir, imp))

        # initialize all services
        for service in mbook_config.get('services', []):
            self._add_service(service)

        self.configuration.update(mbook_config.get('configuration', dict()))

        for metric in mbook_config.get('metrics', []):
            self._add_metric(metric)

    def _add_service(self, service_path):
        package_name, class_name = service_path['module'].rsplit('.', maxsplit=1)
        service_configuration = service_path.get('configuration', dict())

        module_import = importlib.import_module(package_name)
        self.services[service_path['name']] = getattr(module_import, class_name)(service_configuration)

    def _add_metric(self, metric_path):
        package_name, class_name = metric_path.rsplit('.', maxsplit=1)
        self.metrics.append(
            (metric_path, getattr(importlib.import_module(package_name), class_name)(self.services))
        )

    def run(self):
        for path, metric in self.metrics:
            print(f'Collecting metric "{path}"')
            try:
                metric.run()
            except Exception as e:
                if self.configuration.get('stop_on_exception'):
                    raise e
                else:
                    logging.error(f'Catched Exception while executing {metric}', exc_info=e)
