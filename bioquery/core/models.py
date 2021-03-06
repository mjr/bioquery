from django.db import models
from django.utils import timezone

from .managers import CategoryDB, DNADB, PhotoDB, ReferenceDB, CommentDB


class Category(models.Model):
    name = models.CharField("nome", max_length=255)
    description = models.TextField("descrição")

    objects_db = CategoryDB

    class Meta:
        verbose_name_plural = "categorias"
        verbose_name = "categoria"
        ordering = ("name",)

    def __str__(self):
        return self.name


class DNA(models.Model):
    name = models.CharField("nome", max_length=255)
    sequence = models.TextField("sequência")
    user = models.ForeignKey("auth.User", verbose_name="usuário", on_delete=models.CASCADE)

    objects_db = DNADB

    class Meta:
        verbose_name_plural = "DNA's"
        verbose_name = "DNA"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey("auth.User", verbose_name="usuário", on_delete=models.CASCADE)
    file = models.FileField("arquivo")

    objects_db = PhotoDB

    class Meta:
        verbose_name_plural = "fotos"
        verbose_name = "foto"
        ordering = ("user",)

    def __str__(self):
        return self.file.name

    def save_db(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "core_photo" ("user_id", "file") VALUES (%s, %s) RETURNING id',
                [self.user.pk, self.file.name],
            )

            return cursor.fetchone()[0]

    def save(self):
        self.file.save(self.file.name, self.file.file, save=False)
        self.pk = self.save_db()


class Reference(models.Model):
    name = models.CharField("nome", max_length=255)
    title = models.CharField("título", max_length=255)
    date_access = models.DateTimeField("data do acesso")
    user = models.ForeignKey(
        "auth.User", verbose_name="usuário", on_delete=models.CASCADE, null=True, blank=True
    )

    objects_db = ReferenceDB

    class Meta:
        verbose_name_plural = "referências"
        verbose_name = "referência"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Comment(models.Model):
    article = models.ForeignKey("articles.Article", verbose_name="artigo", on_delete=models.CASCADE)
    content = models.TextField("conteúdo")
    user = models.ForeignKey("auth.User", verbose_name="usuário", on_delete=models.CASCADE)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    objects_db = CommentDB

    class Meta:
        verbose_name_plural = "comentários"
        verbose_name = "comentário"
        ordering = ("-created_at",)

    def __str__(self):
        return self.content

    def save_db(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "core_comment" ("article_id", "content", "user_id", "created_at") VALUES (%s, %s, %s, %s) RETURNING id',
                [
                    self.article.pk,
                    self.content,
                    self.user.pk,
                    self.created_at,
                ],
            )

            return cursor.fetchone()[0]

    def save(self):
        self.created_at = timezone.now()
        self.pk = self.save_db()