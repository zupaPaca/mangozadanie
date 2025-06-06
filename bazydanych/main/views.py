from django.shortcuts import render
from pymongo import MongoClient
import pymongo

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
    db = client['skibidi']
    kolekcja = db['Klasy']
    klasy = [klasa for klasa in kolekcja.find({}, {"NazwaKlasy": 1, "_id": 0})]

    if request.method == "POST":
        wybrany = request.POST['wybor']
        liczba = int(request.POST.get('kont'))

        wynik = kolekcja.find({"NazwaKlasy": wybrany})

        wynik_list = list(wynik)
        print(wynik_list[0].get("Uczniowie"))
        lista_uczn = []
        for l in wynik_list[0].get("Uczniowie"):
            lista_uczn.append(l)

        for doc in wynik_list:
            doc['_id'] = str(doc['_id'])

        return render(request, 'wyswietl.html', {"result": wynik_list, "uczniowie": lista_uczn[:liczba], "opcje" : klasy})
    else:
        return render(request, 'wyswietl.html', {"opcje": klasy})

def insert(request):
    db = client["skibidi"]
    Klasy = db['Klasy']
    Uczniowie = db['Uczniowie']

    l = [klas for klas in Klasy.find({}, {"NazwaKlasy": 1, "_id": 0})]
    data = []
    for dat in l:
        data.append(dat.get("NazwaKlasy"))

    ten_exmp = [] # Do przetrzymywania 10 wyników
    for klasy_info in Klasy.find():
        ten_exmp.append(klasy_info)
    for uczniowie_info in Uczniowie.find():
        ten_exmp.append(uczniowie_info)

    ten_exmp = ten_exmp[:10]

    HTML_data = {"data": data, "ten_exmp": ten_exmp}

    if request.method == "POST":
        if request.POST['form_id'] == 'klasa':
            id_klasy = request.POST.get('id_klasy')
            id_ = int(request.POST.get('id_'))

            insert_data = {
                "NazwaKlasy": id_klasy,
                "_id": id_,
                "Uczniowie": []
            }

            x = Klasy.insert_one(insert_data)

        else:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            wiek = int(request.POST.get('wiek'))
            klasa = request.POST["klasa_wyb"]

            uczen_data = {
                "Imie": name,
                "Nazwisko": surname,
                "wiek": wiek,
                "nr_klasy": klasa
            }

            x = Uczniowie.insert_one(uczen_data)
            x = Klasy.update_one({"NazwaKlasy": klasa}, {"$push": {"Uczniowie": uczen_data}})

    return render(request, 'insert.html', context=HTML_data)

def update_mgdb(request):
    db = client["skibidi"]
    Klasy = db['Klasy']
    Uczniowie = db['Uczniowie']

    ten_exmp = []  # Do przetrzymywania 10 wyników
    for klasy_info in Klasy.find():
        ten_exmp.append(klasy_info)
    for uczniowie_info in Uczniowie.find():
        ten_exmp.append(uczniowie_info)

    ten_exmp = ten_exmp[:10]

    if request.method == 'POST':
        if request.POST['form_id'] == "uczen":
            imie = request.POST.get("imie")
            nazwisko = request.POST.get("nazwisko")
            wiek = int(request.POST.get("wiek"))

            location = {"Imie": imie, "Nazwisko": nazwisko}
            values = {"$set": {"wiek": wiek}}

            x = Uczniowie.update_one(location, values)
        else:
            klasa_old = request.POST.get("kla")
            klasa_new = request.POST.get("naz")

            location = {"NazwaKlasy": klasa_old}
            values = {"$set": {"NazwaKlasy": klasa_new}}

            x = Klasy.update_one(location, values)

    return render(request, 'update.html', {"exmp": ten_exmp})

def drop(request):
    if request.method == "POST":
        wybrany = request.POST['wybor']
        db = client['skibidi']
        kolekcja = db['Klasy']
        wynik = kolekcja.find({"NazwaKlasy": wybrany})
        klasy = kolekcja.find()

        wynik_list = list(wynik)

        for doc in wynik_list:
            doc['_id'] = str(doc['_id'])

        return render(request, 'usun.html', {"result": wynik_list, "opcje" : klasy})
    else:

        db = client['skibidi']
        kolekcja = db['Klasy']

        klasy = kolekcja.find()

        klasy_list = list(klasy)

        for doc in klasy_list:
            doc['_id'] = str(doc['_id'])
        return render(request, 'usun.html', {"opcje" : klasy_list})


def dropuczen(request, iducznia):
    if request.method == "POST":
        db = client['skibidi']
        kolekcja = db['Uczniowie']


        result = kolekcja.delete_one({"id": iducznia})

        if result.deleted_count > 0:
            message = "Uczeń został usunięty."
        else:
            message = "Nie znaleziono ucznia o podanym id."

        return render(request, 'usun_ucz.html', {"message": message})


