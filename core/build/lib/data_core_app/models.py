from django.db import models


class Node(models.Model):
    value = models.CharField(max_length=100)


class NodeAttribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)


class Edge(models.Model):
    originNode = models.ForeignKey(Node, related_name='originNode', on_delete=models.CASCADE)
    targetNode = models.ForeignKey(Node, related_name='targetNode', on_delete=models.CASCADE)
