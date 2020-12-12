from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, resolve_url as r

from bioquery.core.models import Category

from .forms import ArticleForm, PhotoForm
from .models import Article


@login_required
def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(request, 'articles/article_form.html', {
        'form': ArticleForm(),
        'photo_form': PhotoForm(),
    })


def create(request):
    form = ArticleForm(request.POST)
    photo_form = PhotoForm(request.POST, request.FILES)

    if not form.is_valid() or not photo_form.is_valid():
        return render(request, 'articles/article_form.html', {'form': form, 'photo_form': photo_form})

    article = form.save(commit=False)
    article.category = Category.objects_db.get(pk=form['category'].data)
    article.user = request.user
    article.save()

    photo = photo_form.save(commit=False)
    photo.user = request.user
    photo.save()

    photos_pks = form['photos'].data
    if photo:
        photos_pks.append(photo.pk)

    Article.objects_db.set_dnas(article.pk, form['dnas'].data)
    Article.objects_db.set_photos(article.pk, photos_pks)

    return redirect(r('articles:detail', slug=article.slug))


def detail(request, slug):
    article = Article.objects_db.get_object_or_404(slug=slug)
    return render(request, 'articles/article_detail.html', {'article': article})
