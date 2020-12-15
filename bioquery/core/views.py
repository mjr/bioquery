from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bioquery.articles.models import Article


@login_required
def pannel(request):
    articles = Article.objects_db.filter_all(user_id=request.user.id)
    return render(request, "pannel.html", {"articles": articles})


def search(request):
    query = request.GET.get("q", "")
    articles = Article.objects_db.filter_by_title_and_content(query)
    return render(request, "search.html", {"query": query, "articles": articles})


def home(request):
    return render(request, "index.html")