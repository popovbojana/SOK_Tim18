from data_core_app.models import *
from data_core_app.services.graphLoadingService import GraphLoadingService
from xml.etree.ElementTree import *


class LoadXML(GraphLoadingService):
    def name(self):
        return 'xml'

    def __init__(self):
        self.references = {}

    def load_graph(self, path: str):
        tree = parse(path)
        root = tree.getroot()
        self.create_element(root)
        self.create_reference_edges()

    def create_element(self, element):
        node = Node(value=element.tag.replace("\n", ""))
        node.save()
        self.parse_tag_attributes(element, node)
        if element.text.strip() == "":
            for child in list(element):
                if len(list(child)) == 0:
                    self.parse_tag_attributes(child, node)
                    nodeAttribute = NodeAttribute(value=child.text.replace("\n", ""), name=child.tag.replace("\n", ""), node=node)
                    nodeAttribute.save()
                else:
                    targetNode = self.create_element(child)
                    edge = Edge(originNode=node, targetNode=targetNode)
                    edge.save()
        return node

    def parse_tag_attributes(self, element, node):
        for attribute in element.items():
            if attribute[0].replace("\n", "") == "references":
                if node in self.references:
                    self.references[node].append(attribute[1].replace("\n", ""))
                else:
                    self.references[node] = [attribute[1].replace("\n", "")]
            else:
                nodeAttribute = NodeAttribute(value=attribute[1].replace("\n", ""), name=attribute[0].replace("\n", ""),
                                              node=node)
                nodeAttribute.save()

    def create_reference_edges(self):
        for node in self.references.keys():
            for referenced_id in self.references[node]:
                for attribute in NodeAttribute.objects.filter(name='id'):
                    if attribute.value == referenced_id:
                        edge = Edge(originNode = node, targetNode = attribute.node)
                        edge.save()

