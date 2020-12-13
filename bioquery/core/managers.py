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
    def all():
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_reference"."id", "core_reference"."name", "core_reference"."title", "core_reference"."date_access" FROM "core_reference" ORDER BY "core_reference"."name" DESC'
            )
            row = cursor.fetchall()

        return [Reference(*reference_tuple) for reference_tuple in row]

    @staticmethod
    def delete(**kwargs):
        from .models import Reference

        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM "core_reference" WHERE {get_where("core_reference", kwargs)}')


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
    def all():
        from .models import DNA

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT "core_dna"."id", "core_dna"."name", "core_dna"."sequence" FROM "core_dna" ORDER BY "core_dna"."name" DESC'
            )
            row = cursor.fetchall()

        return [DNA(*dna_tuple) for dna_tuple in row]


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