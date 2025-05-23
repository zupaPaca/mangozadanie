from django.shortcuts import render
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['skibidi']

print("Collections in 'skibidi':", db.list_collection_names())

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
    if request.method == "POST":
        wybrany = request.POST['wybor']
        db = client['skibidi']
        kolekcja = db['Klasy']
        wynik = kolekcja.find({"NazwaKlasy": wybrany})
        klasy = kolekcja.find()

        wynik_list = list(wynik)

        for doc in wynik_list:
            doc['_id'] = str(doc['_id'])

        return render(request, 'wyswietl.html', {"result": wynik_list, "opcje" : klasy})
    else:

        db = client['skibidi']
        kolekcja = db['Klasy']

        klasy = kolekcja.find()

        klasy_list = list(klasy)

        for doc in klasy_list:
            doc['_id'] = str(doc['_id'])
        return render(request, 'wyswietl.html', {"opcje" : klasy_list})
