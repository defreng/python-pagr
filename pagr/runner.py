from argparse import ArgumentParser
import glob
import importlib.util
import inspect
import os
import sys


def run_folder(argv=None):
    parser = ArgumentParser(description='pagr - the Python Aggregator')
    parser.add_argument('folder', metavar='myfolder', type=str, nargs='+',
                        help='a base folder in which all services/metrics should be executed')

    args = parser.parse_args(argv)

    # save the created services / metric objects and return them later. This allows for better testing.
    created_objects = []

    configuration = dict()
    for key, value in os.environ.items():
        if key.startswith('PAGR_'):
            configuration[key[5:]] = value
    
    for path in args.folder:
        module_name = os.path.basename(os.path.normpath(path))
        abspath = os.path.abspath(path)

        services = dict()
        metrics = dict()

        if not os.path.isdir(abspath):
            raise Exception(f'Given folder {abspath} could not be found')
        
        # import services
        for pyfile in glob.glob(os.path.join(abspath, 'services', '*.py')):
            service_name = module_name + '.services.' + os.path.split(pyfile)[1].rsplit('.py')[0]

            spec = importlib.util.spec_from_file_location(service_name, pyfile)
            service = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(service)

            for name, obj in inspect.getmembers(service):
                if not inspect.isclass(obj):
                    continue
                if not name.endswith('Service'):
                    pass
                
                if name in services:
                    raise Exception(f'Service {name} already exists')
                
                services[name] = obj(configuration)
        
        # import metrics
        for pyfile in glob.glob(os.path.join(abspath, 'metrics', '*.py')):
            service_name = module_name + '.metrics.' + os.path.split(pyfile)[1].rsplit('.py')[0]

            spec = importlib.util.spec_from_file_location(service_name, pyfile)
            service = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(service)

            for name, obj in inspect.getmembers(service):
                if not inspect.isclass(obj):
                    continue
                if not name.endswith('Metric'):
                    pass
                
                if name in metrics:
                    raise Exception(f'Metric {name} already exists')
                
                metrics[name] = m = {
                    'name': name,
                    'instance': obj(services)
                }
                m['instance'].run()

        created_objects.append((abspath, services, metrics))

    return created_objects


if __name__ == '__main__':
    run_folder(sys.argv[1:])
