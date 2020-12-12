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
