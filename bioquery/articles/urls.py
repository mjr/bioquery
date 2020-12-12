from django.urls import path

from .views import new, detail


app_name = "articles"

urlpatterns = [
    path('', new, name='new'),
    path('<str:slug>/', detail, name='detail'),
]