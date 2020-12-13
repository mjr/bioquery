from django.urls import path

from .views import home, pannel, search


urlpatterns = [
    path("", home, name="home"),
    path("painel/", pannel, name="pannel"),
    path("search/", search, name="search"),
]