from django.db import connection
from django.http import Http404

from bioquery.core.utils import get_where, get_set


class ArticleDB:
    @staticmethod
    def get_object_or_404(**kwargs):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "articles_article"."user_id", "articles_article"."category_id", "articles_article"."added_in" FROM "articles_article" WHERE {get_where("articles_article", kwargs)}')
            row = cursor.fetchone()

        if row is None:
            raise Http404

        return Article(*row)

    @staticmethod
    def all():
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute('SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "articles_article"."user_id", "articles_article"."category_id", "articles_article"."added_in" FROM "articles_article" ORDER BY "articles_article"."added_in" DESC')
            row = cursor.fetchall()

        return [Article(*article_tuple) for article_tuple in row]

    @staticmethod
    def filter_by_title_and_content(term):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute('SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "articles_article"."user_id", "articles_article"."category_id", "articles_article"."added_in" FROM "articles_article" WHERE ("articles_article"."title" LIKE %s ESCAPE "\\" OR "articles_article"."content" LIKE %s ESCAPE "\\") ORDER BY "articles_article"."added_in" DESC', [f'%{term}%', f'%{term}%'])
            row = cursor.fetchall()

        return [Article(*article_tuple) for article_tuple in row]

    @staticmethod
    def set_dnas(pk, fks):
        if not fks:
            return

        with connection.cursor() as cursor:
            cursor.execute(f'INSERT OR IGNORE INTO "articles_article_dnas" ("article_id", "dna_id") {get_set(pk, fks)}')

    @staticmethod
    def set_photos(pk, fks):
        if not fks:
            return

        with connection.cursor() as cursor:
            cursor.execute(f'INSERT OR IGNORE INTO "articles_article_photos" ("article_id", "photo_id") {get_set(pk, fks)}')