from django.db import models


class Article(models.Model):
    title = models.CharField('título', max_length=255)
    slug = models.SlugField('slug')
    content = models.TextField('conteúdo')
    user = models.ForeignKey('auth.User', verbose_name='usuário', on_delete=models.CASCADE)
    category = models.ForeignKey('core.Category', verbose_name='categoria', on_delete=models.CASCADE)
    dnas = models.ManyToManyField('core.DNA', verbose_name="DNA's", blank=True)
    photos = models.ManyToManyField('core.Photo', verbose_name='fotos', blank=True)
    added_in = models.DateTimeField('adicionado em', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'artigos'
        verbose_name = 'artigo'
        ordering = ('-added_in',)

    def __str__(self):
        return self.title