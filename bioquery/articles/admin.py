from django.contrib import admin

from bioquery.core.models import Reference, Comment

from .models import Article


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ArticleModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ReferenceInline, CommentInline]


admin.site.register(Article, ArticleModelAdmin)
