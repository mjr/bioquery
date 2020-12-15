from django.db.models import Q
from django.shortcuts import render

from bioquery.articles.models import Article


def pannel(request):
    return render(request, "pannel.html")


def search(request):
    query = request.GET.get("q", "")
    articles = Article.objects_db.filter_by_title_and_content(query)
    return render(request, "search.html", {"query": query, "articles": articles})


def home(request):
    return render(request, "index.html")