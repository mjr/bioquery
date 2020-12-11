from django.db import models


class Category(models.Model):
    name = models.CharField('nome', max_length=255)
    description = models.TextField('descrição')

    class Meta:
        verbose_name_plural = "categorias"
        verbose_name = "categoria"
        ordering = ('name',)

    def __str__(self):
        return self.name


class DNA(models.Model):
    name = models.CharField('nome', max_length=255)
    sequence = models.CharField('sequência', max_length=255)
    user = models.ForeignKey('auth.User', verbose_name='usuário', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "DNA's"
        verbose_name = "DNA"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey('auth.User', verbose_name='usuário', on_delete=models.CASCADE)
    file = models.FileField("arquivo")

    class Meta:
        verbose_name_plural = "fotos"
        verbose_name = "foto"
        ordering = ('user',)

    def __str__(self):
        return self.file.name


class Reference(models.Model):
    name = models.CharField('nome', max_length=255)
    title = models.CharField('título', max_length=255)
    date_access = models.DateTimeField('data do acesso')
    article = models.ForeignKey('articles.Article', verbose_name='artigo', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "referências"
        verbose_name = "referência"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    article = models.ForeignKey('articles.Article', verbose_name='artigo', on_delete=models.CASCADE)
    content = models.TextField('conteúdo')
    user = models.ForeignKey('auth.User', verbose_name='usuário', on_delete=models.CASCADE)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name_plural = "comentários"
        verbose_name = "comentário"
        ordering = ('-created_at',)

    def __str__(self):
        return self.content