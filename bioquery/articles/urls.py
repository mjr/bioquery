from django.urls import path

from .views import (
    new,
    detail,
    references,
    new_reference,
    delete_reference,
    dnas,
    new_dna,
    edit_dna,
    delete_dna,
    delete_article,
    update_article,
    edit_reference,
)


app_name = "articles"

urlpatterns = [
    path("", new, name="new"),
    path("dnas/", dnas, name="dnas"),
    path("dnas/new/", new_dna, name="new_dna"),
    path("dnas/<int:id>/edit/", edit_dna, name="edit_dna"),
    path("references/", references, name="references"),
    path("references/new/", new_reference, name="new_reference"),
    path("references/<int:id>/delete/", delete_reference, name="delete_reference"),
    path("references/<int:id>/edit/", edit_reference, name="edit_reference"),
    path("dnas/<int:id>/delete/", delete_dna, name="delete_dnas"),
    path("<str:slug>/", detail, name="detail"),
    path("<str:slug>/delete/", delete_article, name="delete_article"),
    path("<str:slug>/edit/", update_article, name="edit_article"),
]