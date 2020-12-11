from django.http import Http404
from django.shortcuts import render

from .models import Article


def detail(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'articles/article_detail.html', {'article': article})
