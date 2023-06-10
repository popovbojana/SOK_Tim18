import pkg_resources
from django.apps import AppConfig


class DataCoreAppConfig(AppConfig):
    name = 'data_core_app'
    source_plugins = []
    visualisation_plugins = []

    def ready(self):
        self.source_plugins = load_plugins('source')
        self.visualisation_plugins = load_plugins('visualisation')

def load_plugins(mark):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=mark):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins
