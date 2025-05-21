from django.shortcuts import render
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)


def bazy_danych():
    print(client.list_database_names())
    return client.list_database_names()

def klucze(baza_danych, kolekcja):
    db = client[baza_danych]
    collection = db[kolekcja]

    kluczyki = []

    for document in collection.find():
        kluczyki.append(document.keys())

    return kluczyki

def find(kwerenda, kolekcja, baza_danych):
    db = client[baza_danych]
    collection = db[kolekcja]

    return collection.find(kwerenda)

def update(id ,kwerenda, kolekcja, baza_danych):
    db = client[baza_danych]
    collection = db[kolekcja]

# Create your views here.


def index(request):
    return render(request, 'index.html')

def wyswietl_dane(request):
    if request.method == "GET":
        # kolekcja = request.wybrana_kolekcja
        # baza_danych = request.wybrana_baza_danych
        db = client['Klasy']
        kolekcja = db['NazwaKlasy']
        wynik = kolekcja.find({})
        wynik_list = list(wynik)

        return render(request, 'wyswietl.html', {"result": wynik_list})
    else:
        return render(request, 'wyswietl.html')

def insert(request):
    if request.method == "POST":
        db = client["Klasy"]
        kolekcja = db['NazwaKlasy']


    return render(request, 'insert.html')