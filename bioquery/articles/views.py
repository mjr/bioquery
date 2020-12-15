from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, resolve_url as r
from django.db import transaction
from bioquery.core.models import Category, Photo, Reference, DNA
from django.utils.text import slugify

from .forms import ArticleForm, PhotoForm, ReferenceForm, DNAForm
from .models import Article


@login_required
def delete_dna(request, id):
    DNA.objects_db.delete(id, request.user.id)
    return redirect(r("articles:dnas"))


@login_required
def edit_dna(request, id):
    dna = DNA.objects_db.get(id=id)
    if request.method == "POST":
        form = DNAForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "articles/dna_form.html",
                {"form": form},
            )

        DNA.objects_db.update(dna.id, form.cleaned_data["name"], form.cleaned_data["sequence"])
        return redirect(r("articles:dnas"))
    return render(
        request,
        "articles/dna_form.html",
        {
            "form": DNAForm(initial={"name": dna.name, "sequence": dna.sequence}),
        },
    )


@login_required
def edit_reference(request, id):
    reference = Reference.objects_db.get(id=id)
    if request.method == "POST":
        form = ReferenceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "articles/reference_form.html",
                {"form": form},
            )

        Reference.objects_db.update(
            reference.id,
            form.cleaned_data["name"],
            form.cleaned_data["title"],
            form.cleaned_data["date_access"],
        )
        return redirect(r("articles:references"))
    return render(
        request,
        "articles/reference_form.html",
        {
            "form": ReferenceForm(
                initial={
                    "name": reference.name,
                    "title": reference.title,
                    "date_access": reference.date_access,
                }
            ),
        },
    )


@login_required
def dnas(request):
    dnas = DNA.objects_db.all(user_id=request.user.id)
    return render(
        request,
        "articles/dnas.html",
        {"dnas": dnas},
    )


@login_required
def new_dna(request):
    if request.method == "POST":
        form = DNAForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "articles/dna_form.html",
                {"form": form},
            )
        dnas = form.save(commit=False)
        dnas.user = request.user
        dnas.save()
        return redirect(r("articles:dnas"))
    return render(
        request,
        "articles/dna_form.html",
        {
            "form": DNAForm(),
        },
    )


@login_required
def references(request):
    references = Reference.objects_db.all(user_id=request.user.id)
    return render(
        request,
        "articles/references.html",
        {"references": references},
    )


@login_required
def new_reference(request):
    if request.method == "POST":
        form = ReferenceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "articles/reference_form.html",
                {"form": form},
            )
        dna = form.save(commit=False)
        dna.user = request.user
        dna.save()
        return redirect(r("articles:references"))
    return render(
        request,
        "articles/reference_form.html",
        {
            "form": ReferenceForm(),
        },
    )


@login_required
def delete_reference(request, id):
    Reference.objects_db.delete(id, request.user.id)
    return redirect(r("articles:references"))


@login_required
def new(request):
    if request.method == "POST":
        return create(request)
    return empty_form(request)


@login_required
def update_article(request, slug):
    article = Article.objects_db.get_object_or_404(slug=slug)
    if request.method == "POST":
        return update(article.id, request)
    dnas = DNA.objects_db.all_from_article(article.id)
    references = Reference.objects_db.all_from_article(article.id)
    photo = Photo.objects_db.get_from_article(article.id)

    return empty_form(
        request,
        {
            "title": article.title,
            "content": article.content,
            "category": article.category_id,
            "photo": photo.id,
            "references": [reference.id for reference in references],
            "dnas": [dna.id for dna in dnas],
        },
    )


@login_required
def delete_article(request, slug):
    article = Article.objects_db.get_object_or_404(slug=slug)
    Article.objects_db.delete(article.id, request.user.id)
    return redirect(r("pannel"))


@login_required
def empty_form(request, data={}):
    return render(
        request,
        "articles/article_form.html",
        {
            "form": ArticleForm(initial=data, user=request.user),
            "photo_form": PhotoForm(),
        },
    )


def update(article_id, request):
    form = ArticleForm(request.POST, user=request.user)
    photo_form = PhotoForm(request.POST, request.FILES)

    if not form.is_valid() or not photo_form.is_valid():
        return render(
            request,
            "articles/article_form.html",
            {"form": form, "photo_form": photo_form},
        )

    with transaction.atomic():
        photo = None
        if photo_form["file"].data:
            photo = photo_form.save(commit=False)
            photo.user = request.user
            photo.save()
        elif form["photo"].data:
            photo = Photo.objects_db.get(id=form["photo"].data)

        Article.objects_db.update(
            article_id,
            form.cleaned_data["title"],
            slugify(form.cleaned_data["title"]),
            form.cleaned_data["content"],
            form.cleaned_data["category"],
        )

        if photo:
            Article.objects_db.update_photo(article_id, photo.id)

        Article.objects_db.set_dnas(article_id, form["dnas"].data)
        Article.objects_db.set_references(article_id, form["references"].data)

    return redirect(r("pannel"))


def create(request):
    form = ArticleForm(request.POST, user=request.user)
    photo_form = PhotoForm(request.POST, request.FILES)

    if not form.is_valid() or not photo_form.is_valid():
        return render(
            request,
            "articles/article_form.html",
            {"form": form, "photo_form": photo_form},
        )

    with transaction.atomic():
        photo = None
        if photo_form["file"].data:
            photo = photo_form.save(commit=False)
            photo.user = request.user
            photo.save()
        elif form["photo"].data:
            photo = Photo.objects_db.get(id=form["photo"].data)

        article = form.save(commit=False)
        article.category = Category.objects_db.get(pk=form["category"].data)
        article.user = request.user
        if photo:
            article.photo = photo
        article.save()

        Article.objects_db.set_dnas(article.pk, form["dnas"].data)
        Article.objects_db.set_references(article.pk, form["references"].data)

    return redirect(r("articles:detail", slug=article.slug))


def detail(request, slug):
    article = Article.objects_db.get_complex_or_404(slug=slug)
    references = Reference.objects_db.from_article(article["id"])
    dnas = DNA.objects_db.from_article(article["id"])
    return render(
        request,
        "articles/article_detail.html",
        {"article": article, "references": references, "dnas": dnas},
    )
