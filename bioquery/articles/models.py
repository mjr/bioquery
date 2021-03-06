from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from bioquery.core.models import Category, Photo, Reference

from .managers import ArticleDB


class Article(models.Model):
    title = models.CharField("título", max_length=255)
    slug = models.SlugField("slug")
    content = models.TextField("conteúdo")
    user = models.ForeignKey("auth.User", verbose_name="usuário", on_delete=models.CASCADE)
    category = models.ForeignKey(
        "core.Category", verbose_name="categoria", on_delete=models.CASCADE
    )
    dnas = models.ManyToManyField("core.DNA", verbose_name="DNA's", blank=True)
    photo = models.ForeignKey(
        "core.Photo",
        verbose_name="fotos",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
        default=None,
    )
    references = models.ManyToManyField("core.Reference", verbose_name="referências", blank=True)
    added_in = models.DateTimeField("adicionado em", auto_now_add=True)

    objects_db = ArticleDB

    class Meta:
        verbose_name_plural = "artigos"
        verbose_name = "artigo"
        ordering = ("-added_in",)

    def __str__(self):
        return self.title

    def save_sql(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "articles_article" ("title", "slug", "content", "user_id", "category_id", "photo_id", "added_in") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                [
                    self.title,
                    self.slug,
                    self.content,
                    self.user.pk,
                    self.category.pk,
                    self.photo.pk if self.photo else None,
                    self.added_in,
                ],
            )

            return cursor.fetchone()[0]

    def save_db(self):
        slug = slugify(self.title)
        self.slug = slug[:50] if len(slug) > 50 else slug
        self.added_in = timezone.now()
        self.pk = self.save_sql()