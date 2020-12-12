from django.db.models import Q
from django.shortcuts import render

from bioquery.articles.models import Article


def home(request):
    return render(request, "index.html")


def pannel(request):
    return render(request, "pannel.html")


def search(request):
    return render(request, "search.html")


def new_post(request):
    return render(request, "new_post.html")


def new_dna(request):
    return render(request, "new_post.html")


def new_reference(request):
    return render(request, "new_post.html")
