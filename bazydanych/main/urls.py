from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('wyswietl', views.wyswietl_dane, name='wyswietl'),
    path('insert', views.insert, name='insert'),
    path('update', views.update_mgdb, name='update'),
    path('drop', views.drop, name='drop'),
    path('drop/uczen/<str:imie>/<str:nazwisko>', views.dropuczen, name='dropuczen'),
    path('drop/nauczyciel/<str:imie>/<str:nazwisko>', views.dropnauczyciel, name='dropuczen'),
]