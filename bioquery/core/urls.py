from django.urls import path

from .views import home, pannel


urlpatterns = [
    path("", home, name="home"),
    path("painel/", pannel, name="pannel"),
]