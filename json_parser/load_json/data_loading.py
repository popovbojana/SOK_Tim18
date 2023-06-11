from data_core_app.models import *
from data_core_app.services.graphLoadingService import GraphLoadingService
import json


class JsonDataLoader(GraphLoadingService):

    def name(self):
        return "json"

    def __init__(self):
        self.attributes_to_delete = []
        self.nodes_to_delete = []
        self.counter = 0

    def load_graph(self, path: str):
        file = open(path)
        data = json.load(file)
        self.process_data(data)
        self.load_references()
        file.close()

    def process_data(self, data):
        for key in data.keys():
            node = Node(value=key)
            node.save()
            self.load_node_attributes(data[key], node)

    def load_node_attributes(self, data, node):
        if type(data) == dict:
            for key in data.keys():
                attribute = data[key]
                if type(attribute) is not list and type(attribute) is not dict:
                    attribute = NodeAttribute(name=key, value=attribute, node=node)
                    attribute.save()
                else:
                    new_node = Node(value=key)
                    new_node.save()
                    edge = Edge(originNode=node, targetNode=new_node)
                    edge.save()
                    self.load_children(attribute, new_node)
        elif type(data) == list:
            my_dict = {}
            for i in range(0, len(data)):
                my_dict[i+1] = data[i]
            self.load_node_attributes(my_dict, node)

    def load_children(self, data, node):
        if type(data) is dict:
            self.load_node_attributes(data, node)
        elif type(data) is list:
            for element in data:
                if type(element) is dict:
                    if len(element.keys()) == 1:
                        new_node = Node(value=list(element.keys())[0])
                        new_node.save()
                        self.load_node_attributes(element[new_node.value], new_node)
                    else:
                        new_node = Node(value=f"_object_{self.counter}")
                        self.counter += 1
                        new_node.save()
                        self.load_node_attributes(element, new_node)
                    edge = Edge(originNode=node, targetNode=new_node)
                    edge.save()
                elif type(element) is list:
                    new_node = Node(value=f"_object_{self.counter}")
                    self.counter += 1
                    new_node.save()
                    edge = Edge(originNode=node, targetNode=new_node)
                    edge.save()
                    self.load_children(element, new_node)
                else:
                    new_attribute = NodeAttribute(name=f"{data.index(element)+1}", value=element, node=node)
                    new_attribute.save()

    def load_references(self):
        self.load_id_references()
        self.load_object_references()
        self.clear_redundant_attributes()
        self.clear_redundant_nodes()

    def load_object_references(self):
        for node_object in Node.objects.all():
            if "_object_" in node_object.value:
                for node in Node.objects.all():
                    if node.value != node_object.value and\
                        self.nodes_have_same_attributes(node, node_object) and\
                            self.nodes_contain_same_children(node, node_object):
                        self.nodes_to_delete.append(node_object)
                        for edge in Edge.objects.all().filter(targetNode=node_object):
                            new_edge = Edge(originNode=edge.originNode, targetNode=node)
                            new_edge.save()

    def load_id_references(self):
        for node in Node.objects.all():
            for attribute in NodeAttribute.objects.all().filter(value=node.value):
                self.attributes_to_delete.append(attribute)
                if attribute.name.isdigit():
                    new_edge = Edge(originNode=attribute.node, targetNode=node)
                    new_edge.save()
                else:
                    attribute_name_node = Node(value=attribute.name)
                    attribute_name_node.save()
                    new_edge = Edge(originNode=attribute.node, targetNode=attribute_name_node)
                    new_edge.save()
                    attribute_value_edge = Edge(originNode=attribute_name_node, targetNode=node)
                    attribute_value_edge.save()

    def clear_redundant_attributes(self):
        for attribute in self.attributes_to_delete:
            attribute.delete()
        self.attributes_to_delete = []

    def clear_redundant_nodes(self):
        for node in self.nodes_to_delete:
            self.clear_nodes_children(node)
            node.delete()
        self.nodes_to_delete = []

    def clear_nodes_children(self, node):
        edges = Edge.objects.all().filter(originNode=node)
        for edge in edges:
            self.clear_nodes_children(edge.targetNode)
            edge.targetNode.delete()

    def nodes_have_same_attributes(self, node1, node2):
        attributes1 = NodeAttribute.objects.all().filter(node=node1)
        attributes2 = NodeAttribute.objects.all().filter(node=node2)
        if len(attributes1) != len(attributes2):
            return False
        for attribute1 in attributes1:
            if not self.attributes_contain_attribute(attributes2, attribute1):
                return False
        return True

    def nodes_contain_same_children(self, node1, node2):
        edges1 = Edge.objects.all().filter(originNode=node1)
        edges2 = Edge.objects.all().filter(originNode=node2)
        if len(edges1) != len(edges2):
            return False
        for i in range(len(edges1)):
            if not self.nodes_have_same_attributes(edges1[i].targetNode, edges2[i].targetNode):
                return False
            if not self.nodes_contain_same_children(edges1[i].targetNode, edges2[i].targetNode):
                return False
        return True

    @staticmethod
    def attributes_contain_attribute(attributes, attribute):
        for attr in attributes:
            if attr.name == attribute.name and attr.value == attribute.value:
                return True
        return False
