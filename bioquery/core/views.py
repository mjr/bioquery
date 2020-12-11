from django.db.models import Q
from django.shortcuts import render

from bioquery.articles.models import Article


def home(request):
    query = request.GET.get('q', '')
    articles = Article.objects.all()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'index.html', {'query': query, 'articles': articles})