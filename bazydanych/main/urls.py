from django.contrib import admin
from django.urls import path
import
urlpatterns = [
    path('', views.index, name='index'),
    path('wyswietl', views.wyswietl, name='wyswietl'),
]