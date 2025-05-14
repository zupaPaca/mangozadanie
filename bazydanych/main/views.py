from django.shortcuts import render
import pymongo


connection_string = "mongodb://localhost:27017"

client = pymongo.MongoClient(connection_string)

def bazy_danych():
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
    if request.method == "POST":
        kolekcja = request.wybrana_kolekcja
        baza_danych = request.wybrana_baza_danych
        wynik = find("", kolekcja, baza_danych)
        return render(request, 'index.html', {"result": wynik})
    else:
        return render(request, 'index.html')