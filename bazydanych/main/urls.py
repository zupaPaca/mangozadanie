from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('wyswietl', views.wyswietl_dane, name='wyswietl'),
]