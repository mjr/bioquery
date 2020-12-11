from django.contrib import admin

from .models import Category, DNA, Photo, Reference, Comment


admin.site.register([Category, DNA, Photo, Reference, Comment])
