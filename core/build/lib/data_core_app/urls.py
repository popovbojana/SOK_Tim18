from django.urls import path

from data_core_app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('view', views.view, name='view'),
    path('search', views.search, name='search'),
    path('filter', views.filter, name='filter')
]
