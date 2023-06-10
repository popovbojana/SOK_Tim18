import os
from jinja2 import PackageLoader, FileSystemLoader, Environment
from data_core_app.services.visualizationService import VisualizationService

class SimpleVisualisation(VisualizationService):

    def name(self):
        return "SimpleVisualisation"

    def load(self):
        p = os.path.dirname(__file__)
        path = os.path.join(p, "templates")
        env = Environment(loader=FileSystemLoader(searchpath=path))
        template = env.get_template('simpleVisual.html')
        return template
