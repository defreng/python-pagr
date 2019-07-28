from argparse import ArgumentParser
import glob
import importlib.util
import inspect
import os
import sys
import pkgutil


class ServiceLoader:
    def __init__(self, folder_path):
        self._instances = dict()

        self.folder_path = folder_path
        self.configuration = dict()
        for key, value in os.environ.items():
            if key.startswith('PAGR_'):
                self.configuration[key[5:]] = value

        self.preload_folder_services()

    def preload_folder_services(self):
        module_name = os.path.basename(os.path.normpath(self.folder_path))
        abspath = os.path.abspath(self.folder_path)

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

                if name in self._instances:
                    raise Exception(f'Service {name} already exists')

                self._instances[name] = obj(self.configuration)

    def __getitem__(self, item):
        if item in self._instances:
            return self._instances[item]

        # first, try to load internal service
        from pagr import services as internal_services

        for importer, modname, ispkg in pkgutil.iter_modules(internal_services.__path__):
            try:
                service = importer.find_module(modname).load_module(modname)
            except ImportError:
                continue

            for name, obj in inspect.getmembers(service):
                if name != item:
                    continue
                if not inspect.isclass(obj):
                    continue

                self._instances[name] = obj(self.configuration)
                return self._instances[name]

    def __len__(self):
        return len(self._instances)


def run_folder(argv=None):
    parser = ArgumentParser(description='pagr - the Python Aggregator')
    parser.add_argument('folder', metavar='myfolder', type=str, nargs='+',
                        help='a base folder in which all services/metrics should be executed')

    args = parser.parse_args(argv)

    # save the created services / metric objects and return them later. This allows for better testing.
    created_objects = []
    
    for path in args.folder:
        module_name = os.path.basename(os.path.normpath(path))
        abspath = os.path.abspath(path)

        services = ServiceLoader(path)
        metrics = dict()

        if not os.path.isdir(abspath):
            raise Exception(f'Given folder {abspath} could not be found')
        
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
