import importlib
import logging
import os
import re
from argparse import ArgumentParser

import sys
import yaml


SERVICE_REGISTRY = dict()


def add_service(service_path):
    package_name, class_name = service_path['module'].rsplit('.', maxsplit=1)
    service_configuration = service_path.get('configuration', dict())

    module_import = importlib.import_module(package_name)
    SERVICE_REGISTRY[service_path['name']] = getattr(module_import, class_name)(service_configuration)


def run_metric(metric_path):
    package_name, class_name = metric_path.rsplit('.', maxsplit=1)
    metric = getattr(importlib.import_module(package_name), class_name)(SERVICE_REGISTRY)

    metric.run()


def run_mbook(filename):
    # add additional resolver to interpret environment variables within the yaml file
    env_matcher = re.compile(r'^\${([^}^{]+)}$')

    def env_constructor(loader, node):
        match = env_matcher.match(node.value)
        return os.environ.get(match.group(1))

    yaml.add_implicit_resolver('!env', env_matcher)
    yaml.add_constructor('!env', env_constructor)
    with open(filename) as f:
        mbook_config = yaml.load(f)

    # initialize all services
    for service in mbook_config.get('services', []):
        add_service(service)

    configuration = mbook_config.get('configuration', dict())

    # add the configuration directory to sys.path, such that we can load metrics from there
    sys.path.append(os.path.dirname(filename))

    # execute all metrics
    for metric in mbook_config.get('metrics', []):
        print(f'Collecting metric "{metric}"')
        try:
            run_metric(metric)
        except Exception as e:
            if configuration.get('stop_on_exception'):
                raise e
            else:
                logging.error(f'Catched Exception while executing {metric}', exc_info=e)


def run(args=None):
    parser = ArgumentParser(description='pagr - the Python Aggregator')
    parser.add_argument('mbooks', metavar='my_mbook.yaml', type=str, nargs='+',
                        help='a metricbook configuration file to execute')

    args = parser.parse_args(args)
    for mbook in args.mbooks:
        run_mbook(mbook)
