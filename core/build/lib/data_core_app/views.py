import os
import traceback

from django.apps import apps
from django.contrib import messages
from django.shortcuts import render, redirect
from data_core_app.models import *


def home(request):
    return render(request, "index.html", {})


def view(request):
    clear()
    source_plugins = apps.get_app_config('data_core_app').source_plugins
    visualisation_plugins = apps.get_app_config('data_core_app').visualisation_plugins
    try:
        parse_path(request)
        run_source_plugins(source_plugins, request)
        html = run_visualisation_plugins(visualisation_plugins, request)
        nodes, attributes, edges = Node.objects.all(), NodeAttribute.objects.all(), Edge.objects.all()
        roots = get_roots(nodes, edges)
        node_children = get_nodes_children(nodes, edges)
        attribute_children = get_nodes_attributes(nodes, attributes)
        isolated_nodes = get_isolated_nodes(nodes, edges)
        return render(request, "treeView.html", {"template": html, "roots": roots, "node_children": node_children,
                                                 "attribute_children": attribute_children,
                                                 "isolated_nodes": isolated_nodes,
                                                 "nodesList": nodes, "edgesList": edges})
    except FileNotFoundError:
        messages.error(request, "File doesn't exist!")
        return render(request, "index.html")
    except Exception as e:
        traceback.print_exc()
        return redirect('home')


def search(request):
    try:
        search_query = request.POST['search']
        for node in Node.objects.all():
            remove = True
            for attribute in NodeAttribute.objects.all():
                if attribute.node == node and search_query.lower() in attribute.value.lower():
                    remove = False
                    break
            if remove:
                node.delete()
        nodes, attributes, edges = Node.objects.all(), NodeAttribute.objects.all(), Edge.objects.all()
        html = template.render(nodesList=nodes, attributesList=attributes, edgesList=edges)
        roots = get_roots(nodes, edges)
        node_children = get_nodes_children(nodes, edges)
        attribute_children = get_nodes_attributes(nodes, attributes)
        isolated_nodes = get_isolated_nodes(nodes, edges)
        return render(request, "treeView.html", {"template": html, "roots": roots, "node_children": node_children,
                                                 "attribute_children": attribute_children,
                                                 "isolated_nodes": isolated_nodes,
                                                 "nodesList": nodes, "edgesList": edges})
    except NameError:
        messages.error(request, "Graph not loaded!")
        return render(request, "index.html")


def filter(request):
    try:
        input = (request.POST['filter'])
        input = input.split(" ")
        queryAttribute, operator, queryValue = input[0], input[1], str(input[2])

        for node in Node.objects.all():
            remove = True
            for attribute in NodeAttribute.objects.filter(name=queryAttribute):
                if operator == "==":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV == qV:
                            remove = False
                            break
                elif operator == ">":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV > qV:
                            remove = False
                            break
                elif operator == ">=":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV >= qV:
                            remove = False
                            break
                elif operator == "<":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV < qV:
                            remove = False
                            break
                elif operator == "<=":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV <= qV:
                            remove = False
                            break
                elif operator == "!=":
                    if attribute.node == node:
                        aV, qV = fixType(attribute.value, queryValue)
                        if aV != qV:
                            remove = False
                            break
            if remove:
                node.delete()
        nodes, attributes, edges = Node.objects.all(), NodeAttribute.objects.all(), Edge.objects.all()
        html = template.render(nodesList=nodes, attributesList=attributes, edgesList=edges)
        roots = get_roots(nodes, edges)
        node_children = get_nodes_children(nodes, edges)
        attribute_children = get_nodes_attributes(nodes, attributes)
        isolated_nodes = get_isolated_nodes(nodes, edges)
        return render(request, "treeView.html", {"template": html, "roots": roots, "node_children": node_children,
                                                 "attribute_children": attribute_children, "isolated_nodes": isolated_nodes,
                                                 "nodesList": nodes, "edgesList": edges})
    except NameError:
        messages.error(request, "Graph not loaded!")
        return render(request, "index.html")
    except IndexError:
        try:
            messages.error(request, "Bad filter arguments!")
            html = template.render(nodesList=Node.objects.all(), attributesList=NodeAttribute.objects.all(),
                                   edgesList=Edge.objects.all())
            return render(request, "treeView.html", {"template": html, "roots": get_roots(Node.objects.all(), Edge.objects.all()),
                                                     "node_children": get_nodes_children(Node.objects.all(), Edge.objects.all()),
                                                     "attribute_children": get_nodes_attributes(Node.objects.all(), NodeAttribute.objects.all()),
                                                     "isolated_nodes": get_isolated_nodes(Node.objects.all(), Edge.objects.all()),
                                                     "nodesList": Node.objects.all(), "edgesList": Edge.objects.all()})
        except NameError:
            messages.error(request, "Graph not loaded!")
            return render(request, "index.html")


def fixType(val1, val2):
    if val1.isnumeric() and val2.isnumeric():
        val1 = float(val1)
        val2 = float(val2)
    else:
        val1 = val1.lower()
        val2 = val2.lower()
    return val1, val2


def run_source_plugins(source_plugins, request):
    for plugin in source_plugins:
        if plugin.name() == request.POST['loader']:
            plugin.load_graph(path)


def run_visualisation_plugins(visualisation_plugins, request):
    for plugin in visualisation_plugins:
        if plugin.name() == request.POST['visualisation']:
            global template
            template = plugin.load()
    html = template.render(nodesList=Node.objects.all(), attributesList=NodeAttribute.objects.all(),
                           edgesList=Edge.objects.all())
    return html


def parse_path(request):
    working_directory = os.path.dirname(__file__)
    static_directory = os.path.join(working_directory, "static")
    global path
    path = request.POST['path']
    path = os.path.join(static_directory, path)


def clear():
    Node.objects.all().delete()
    Edge.objects.all().delete()
    NodeAttribute.objects.all().delete()


def get_nodes_children(nodes, edges):
    node_children = {}
    for node in nodes:
        childrenList = []
        for edge in edges:
            if edge.originNode == node:
                childrenList.append(edge.targetNode)
        node_children[node.id] = childrenList
    return node_children


def get_nodes_attributes(nodes, attributes):
    attribute_children = {}
    for node in nodes:
        children_list = []
        for attr in attributes:
            if attr.node == node:
                children_list.append(attr)
        attribute_children[node.id] = children_list
    return attribute_children


def get_roots(nodes, edges):
    roots = []
    for edge in edges:
        if roots.count(edge.originNode) == 0:
            roots.append(edge.originNode)
    for edge in edges:
        if roots.count(edge.targetNode) > 0:
            roots.remove(edge.targetNode)
    if len(roots) == 0:
        root = find_node_with_most_edges(nodes, edges)
        if root is not None:
            roots.append(root)
    return roots


def find_node_with_most_edges(nodes, edges):
    maxEdges = 0
    root = None
    for node in nodes:
        edges_num = 0
        for edge in edges:
            if edge.originNode == node:
                edges_num += 1
        if edges_num > maxEdges:
            root = node
            maxEdges = edges_num
    return root


def get_isolated_nodes(nodes, edges):
    isolated_nodes = []
    for node in nodes:
        connected_node = False
        for edge in edges:
            if edge.originNode == node or edge.targetNode == node:
                connected_node = True
        if not connected_node:
            isolated_nodes.append(node)
    return isolated_nodes

