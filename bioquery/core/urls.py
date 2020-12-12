from django.urls import path

from .views import home, pannel, search, new_post, new_dna, new_reference


urlpatterns = [
    path("", home, name="home"),
    path("pesquisa/", pannel, name="pannel"),
    path("painel/", pannel, name="pannel"),
    path("search/", search, name="search"),
    path("nova-postagem/", new_post, name="new_post"),
    path("novo-dna/", new_dna, name="new_dna"),
    path("nova-referencia/", new_reference, name="new_reference"),
]