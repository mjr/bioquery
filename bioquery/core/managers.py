from django.db import connection

from bioquery.core.utils import get_where


class ReferenceDB:
    @staticmethod
    def get(**kwargs):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT "core_reference"."id", "core_reference"."name", "core_reference"."title", "core_reference"."date_access" FROM "core_reference" WHERE {get_where("core_reference", kwargs)}'
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Reference(*row)

    @staticmethod
    def from_article(article_id):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT "core_reference"."id", "core_reference"."name", "core_reference"."title", "core_reference"."date_access" FROM "core_reference"
                INNER JOIN "articles_article_references" on "core_reference"."id"="articles_article_references"."reference_id" and "articles_article_references"."article_id"=%s
                """
                % article_id
            )
            row = cursor.fetchall()

        if row is None:
            return None

        return [Reference(*reference_tuple) for reference_tuple in row]

    @staticmethod
    def all(**kwargs):
        from .models import Reference

        query = "WHERE " + get_where("core_reference", kwargs) if len(kwargs) > 0 else ""
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_reference"."id", "core_reference"."name", "core_reference"."title", "core_reference"."date_access" FROM "core_reference" %s ORDER BY "core_reference"."name" DESC'
                % query
            )
            row = cursor.fetchall()

        return [Reference(*reference_tuple) for reference_tuple in row]

    @staticmethod
    def delete(reference_id, user_id):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM "articles_article_references" WHERE "articles_article_references"."reference_id" = %s;
                DELETE FROM "core_reference" WHERE "core_reference"."id" = %s and "core_reference"."user_id" = %s"""
                % (reference_id, reference_id, user_id)
            )

    def update(dna_id, name, title, date_access):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE "core_reference" SET "name" = '%s', "title" = '%s', "date_access" = '%s' WHERE "core_reference"."id" = %s"""
                % (name, title, date_access, dna_id)
            )


class CategoryDB:
    @staticmethod
    def get(**kwargs):
        from .models import Category

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT "core_category"."id", "core_category"."name", "core_category"."description" FROM "core_category" WHERE {get_where("core_category", kwargs)}'
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(*row)

    @staticmethod
    def all():
        from .models import Category

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_category"."id", "core_category"."name", "core_category"."description" FROM "core_category" ORDER BY "core_category"."name" DESC'
            )
            row = cursor.fetchall()

        return [Category(*category_tuple) for category_tuple in row]


class DNADB:
    @staticmethod
    def get(**kwargs):
        from .models import DNA

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT "core_dna"."id", "core_dna"."name", "core_dna"."sequence" FROM "core_dna" WHERE {get_where("core_dna", kwargs)}'
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return DNA(*row)

    @staticmethod
    def from_article(article_id):
        from .models import DNA

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT "core_dna"."id", "core_dna"."name", "core_dna"."sequence" FROM "core_dna"
                LEFT JOIN "articles_article_dnas" on "core_dna"."id"="articles_article_dnas"."dna_id" and "articles_article_dnas"."article_id"=%s
                """
                % article_id
            )
            row = cursor.fetchall()

        if row is None:
            return None

        return [DNA(*dna_tuple) for dna_tuple in row]

    @staticmethod
    def all(**kwargs):
        from .models import DNA

        query = "WHERE " + get_where("core_dna", kwargs) if len(kwargs) > 0 else ""
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_dna"."id", "core_dna"."name", "core_dna"."sequence" FROM "core_dna" %s ORDER BY "core_dna"."name" DESC'
                % query
            )
            row = cursor.fetchall()

        return [DNA(*dna_tuple) for dna_tuple in row]

    @staticmethod
    def delete(dna_id, user_id):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """
            DELETE FROM "articles_article_dnas" WHERE "articles_article_dnas"."dna_id" = %s;
            DELETE FROM "core_dna" WHERE "core_dna"."id"= %s and "core_dna"."user_id"=%s """
                % (dna_id, dna_id, user_id)
            )

    def update(dna_id, name, sequence):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE "core_dna" SET "name" = '%s', "sequence" = '%s' WHERE "core_dna"."id" = %s"""
                % (name, sequence, dna_id)
            )


class PhotoDB:
    @staticmethod
    def get(**kwargs):
        from .models import Photo

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT "core_photo"."id", "core_photo"."user_id", "core_photo"."file" FROM "core_photo" WHERE {get_where("core_photo", kwargs)}'
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Photo(*row)

    @staticmethod
    def all():
        from .models import Photo

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_photo"."id", "core_photo"."user_id", "core_photo"."file" FROM "core_photo" ORDER BY "core_photo"."id" DESC'
            )
            row = cursor.fetchall()

        return [Photo(*photo_tuple) for photo_tuple in row]