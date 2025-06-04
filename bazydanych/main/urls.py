from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('wyswietl', views.wyswietl_dane, name='wyswietl'),
    path('insert', views.insert, name='insert'),
    path('drop', views.drop, name='drop'),
    path('drop/uczen/<int:iducznia>', views.dropuczen, name='dropuczen'),
]