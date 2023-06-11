import os

from jinja2 import PackageLoader, FileSystemLoader, Environment

from data_core_app.services.visualizationService import VisualizationService


class VisualisationComplex(VisualizationService):

    def name(self):
        return "VisualisationComplex"

    def load(self):
        p = os.path.dirname(__file__)
        path = os.path.join(p, "templates")
        env = Environment(loader=FileSystemLoader(searchpath=path))
        # ucitavanje template-a
        template = env.get_template('complex.html')
        return template