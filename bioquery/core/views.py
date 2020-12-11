from django.db.models import Q
from django.shortcuts import render

from bioquery.articles.models import Article


def home(request):

    return render(request, "index.html")
