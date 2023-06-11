from django.contrib import admin

from data_core_app.models import *

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    pass


@admin.register(NodeAttribute)
class NodeAttributeAdmin(admin.ModelAdmin):
    pass
