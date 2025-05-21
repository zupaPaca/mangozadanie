from django.shortcuts import render
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
print("Client")
print(client)

db = client['skibidi']
print("db")
print(db)
kolekcja = db['Klasy']['NazwaKlasy']
print("Kolekcja")
print(kolekcja)
wynik = kolekcja.find({})
print("wynik")
print(wynik)
wynik_list = list(wynik)
print("wynik listy")
print(wynik_list)

def bazy_danych():
    print(client.list_database_names())
    return client.list_database_names()

def klucze(baza_danych, kolekcja):
    db = client[baza_danych]
    collection = db[kolekcja]

    kluczyki = []

    for document in collection.find():
        kluczyki.append(document.keys())
    print("kluczyki")
    print(kluczyki)
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
        db = client['skibidi']
        kolekcja = db['Klasy']['NazwaKlasy']
        wynik = kolekcja.find({})
        wynik_list = list(wynik)
        print("wynik listy")
        print(wynik_list)
        return render(request, 'wyswietl.html', {"result": wynik_list})
    else:
        return render(request, 'wyswietl.html')