from django.urls import path

from .views import new, detail, references, new_reference, delete_reference, dnas, new_dna


app_name = "articles"

urlpatterns = [
    path("", new, name="new"),
    path("dnas/", dnas, name="dnas"),
    path("dnas/new/", new_dna, name="new_dna"),
    path("references/", references, name="references"),
    path("references/new/", new_reference, name="new_reference"),
    path("references/<int:id>/delete/", delete_reference, name="delete_reference"),
    path("<str:slug>/", detail, name="detail"),
]