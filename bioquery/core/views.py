from django.db.models import Q
from django.shortcuts import render

from bioquery.articles.models import Article


def home(request):
    query = request.GET.get('q', '')
    articles = []
    if query:
        articles = Article.objects_db.filter_by_title_and_content(query)
    else:
        articles = Article.objects_db.all()
    return render(request, 'index.html', {'query': query, 'articles': articles})


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
