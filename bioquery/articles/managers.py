from django.db import connection
from django.http import Http404

from bioquery.core.utils import get_where, get_set


class ArticleDB:
    @staticmethod
    def get_object_or_404(**kwargs):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "articles_article"."user_id", "articles_article"."category_id", "articles_article"."added_in" FROM "articles_article" WHERE {get_where("articles_article", kwargs)}'
            )
            row = cursor.fetchone()

        if row is None:
            raise Http404

        return Article(*row)

    @staticmethod
    def get_complex_or_404(**kwargs):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "auth_user"."username", "core_category"."name", "articles_article"."added_in", "core_photo"."file" FROM "articles_article"
                INNER JOIN "core_photo" on "core_photo"."id"="articles_article"."photo_id"
                INNER JOIN "core_category" on "core_category"."id"="articles_article"."category_id"
                INNER JOIN "auth_user" on "auth_user"."id"="articles_article"."user_id"
                WHERE %s
                """
                % get_where("articles_article", kwargs),
            )
            row = cursor.fetchone()

        if row is None:
            raise Http404

        return {
            "id": row[0],
            "title": row[1],
            "slug": row[2],
            "content": row[3],
            "author": row[4],
            "category": row[5],
            "date": row[6],
            "photo": row[7],
        }

    @staticmethod
    def filter_all(**kwargs):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "auth_user"."username", "core_category"."name", "articles_article"."added_in", "core_photo"."file" FROM "articles_article"
                INNER JOIN "core_photo" on "core_photo"."id"="articles_article"."photo_id"
                INNER JOIN "core_category" on "core_category"."id"="articles_article"."category_id"
                INNER JOIN "auth_user" on "auth_user"."id"="articles_article"."user_id"
                WHERE %s
                """
                % get_where("articles_article", kwargs),
            )
            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "slug": row[2],
                "content": row[3],
                "author": row[4],
                "category": row[5],
                "date": row[6],
                "photo": row[7],
            }
            for row in rows
        ]

    @staticmethod
    def all():
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "articles_article"."user_id", "articles_article"."category_id", "articles_article"."added_in" FROM "articles_article" ORDER BY "articles_article"."added_in" DESC'
            )
            row = cursor.fetchall()

        return [Article(*article_tuple) for article_tuple in row]

    @staticmethod
    def filter_by_title_and_content(term):
        from .models import Article

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT "articles_article"."id", "articles_article"."title", "articles_article"."slug", "articles_article"."content", "auth_user"."username", "core_category"."name", "articles_article"."added_in", "core_photo"."file" FROM "articles_article"
                INNER JOIN "core_photo" on "core_photo"."id"="articles_article"."photo_id"
                INNER JOIN "core_category" on "core_category"."id"="articles_article"."category_id"
                INNER JOIN "auth_user" on "auth_user"."id"="articles_article"."user_id"
                LEFT JOIN "articles_article_references" on "articles_article_references"."article_id"="articles_article"."id"
                LEFT JOIN "core_reference" on "core_reference"."id"="articles_article_references"."reference_id"
                LEFT JOIN "articles_article_dnas" on "articles_article_dnas"."article_id"="articles_article"."id"
                LEFT JOIN "core_dna" on "core_dna"."id"="articles_article_dnas"."dna_id"
                WHERE ("articles_article"."title" LIKE %s ESCAPE '\\' OR "articles_article"."content" LIKE %s ESCAPE '\\' OR "core_dna"."name" LIKE %s ESCAPE '\\' OR "core_dna"."sequence" LIKE %s ESCAPE '\\'
                OR "core_reference"."name" LIKE %s ESCAPE '\\' OR "core_reference"."title" LIKE %s ESCAPE '\\')
                ORDER BY "articles_article"."added_in" DESC""",
                [f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"],
            )
            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "slug": row[2],
                "content": row[3],
                "author": row[4],
                "category": row[5],
                "date": row[6],
                "photo": row[7],
            }
            for row in rows
        ]

    @staticmethod
    def delete(article_id, user_id):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM "articles_article_references" WHERE "articles_article_references"."article_id" = %s;
                DELETE FROM "articles_article_dnas" WHERE "articles_article_dnas"."article_id" = %s;
                DELETE FROM "articles_article" WHERE "articles_article"."id"= '%s' and "articles_article"."user_id"=%s """
                % (article_id, article_id, article_id, user_id)
            )

    @staticmethod
    def set_dnas(pk, fks):
        if not fks:
            return

        with connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO "articles_article_dnas" ("article_id", "dna_id") {get_set(pk, fks)}'
            )

    @staticmethod
    def set_references(pk, fks):
        if not fks:
            return

        with connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO "articles_article_references" ("article_id", "reference_id") {get_set(pk, fks)}'
            )
