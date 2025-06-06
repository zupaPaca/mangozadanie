from django.shortcuts import render, redirect
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
        lista_uczn = []
        lista_naucz = []


        if wynik_list:

            for l in wynik_list[0].get("Uczniowie", []):
                lista_uczn.append(l)


            for p in wynik_list[0].get("Nauczyciele", []):
                lista_naucz.append(p)


            for doc in wynik_list:
                doc['_id'] = str(doc['_id'])

        return render(request, 'wyswietl.html', {
            "result": wynik_list,
            "uczniowie": lista_uczn[:liczba],
            "nauczyciele": lista_naucz,
            "opcje": klasy
        })
    else:
        return render(request, 'wyswietl.html', {"opcje": klasy})


def insert(request):
    db = client["skibidi"]
    Klasy = db['Klasy']
    Uczniowie = db['Uczniowie']
    Nauczyciele = db['Nauczyciele']


    l = [klas for klas in Klasy.find({}, {"NazwaKlasy": 1, "_id": 0})]
    data = [dat.get("NazwaKlasy") for dat in l]


    ten_exmp = []
    for klasy_info in Klasy.find():
        ten_exmp.append(klasy_info)
    for uczniowie_info in Uczniowie.find():
        ten_exmp.append(uczniowie_info)
    for nauczyciele_info in Nauczyciele.find():
        ten_exmp.append(nauczyciele_info)

    ten_exmp = ten_exmp[:10]

    HTML_data = {"data": data, "ten_exmp": ten_exmp}

    if request.method == "POST":

        if request.POST['form_id'] == 'klasa':
            id_klasy = request.POST.get('id_klasy')
            id_ = int(request.POST.get('id_'))

            insert_data = {
                "NazwaKlasy": id_klasy,
                "_id": id_,
                "Uczniowie": [],
                "Nauczyciele": []
            }

            x = Klasy.insert_one(insert_data)


        elif request.POST['form_id'] == 'uczen':
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


        elif request.POST['form_id'] == 'nauczyciel':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            przedmiot = request.POST.get('przedmiot')
            nr_klasy = request.POST["klasa_wyb"]

            nauczyciel_data = {
                "Imie": name,
                "Nazwisko": surname,
                "Przedmiot": przedmiot,
                "NrKlasy": nr_klasy
            }


            x = Nauczyciele.insert_one(nauczyciel_data)

            x = Klasy.update_one({"NazwaKlasy": nr_klasy}, {"$push": {"Nauczyciele": nauczyciel_data}})

        return redirect('insert')

    return render(request, 'insert.html', context=HTML_data)

def update_mgdb(request):
    db = client["skibidi"]
    Klasy = db['Klasy']
    Uczniowie = db['Uczniowie']
    Nauczyciele = db['Nauczyciele']

    ten_exmp = []
    for klasy_info in Klasy.find():
        ten_exmp.append(klasy_info)
    for uczniowie_info in Uczniowie.find():
        ten_exmp.append(uczniowie_info)
    for nauczyciele_info in Nauczyciele.find():
        ten_exmp.append(nauczyciele_info)

    ten_exmp = ten_exmp[:10]

    if request.method == 'POST':
        if request.POST['form_id'] == "uczen":
            imie = request.POST.get("imie")
            nazwisko = request.POST.get("nazwisko")
            wiek = int(request.POST.get("wiek"))

            location = {"Imie": imie, "Nazwisko": nazwisko}
            values = {"$set": {"wiek": wiek}}


            x = Uczniowie.update_one(location, values)


            Klasy.update_many(
                {"Uczniowie": {"$elemMatch": {"Imie": imie, "Nazwisko": nazwisko}}},
                {"$set": {"Uczniowie.$.wiek": wiek}}
            )

        elif request.POST['form_id'] == "nauczyciel":
            nauczyciel_imie = request.POST.get("nauczyciel_imie")
            nauczyciel_nazwisko = request.POST.get("nauczyciel_nazwisko")
            przedmiot = request.POST.get("przedmiot")

            location = {"Imie": nauczyciel_imie, "Nazwisko": nauczyciel_nazwisko}
            values = {"$set": {"Przedmiot": przedmiot}}


            x = Nauczyciele.update_one(location, values)


            Klasy.update_many(
                {"Nauczyciele": {"$elemMatch": {"Imie": nauczyciel_imie, "Nazwisko": nauczyciel_nazwisko}}},
                {"$set": {"Nauczyciele.$.Przedmiot": przedmiot}}
            )

        elif request.POST['form_id'] == "klasa":
            klasa_old = request.POST.get("kla")
            klasa_new = request.POST.get("naz")


            location = {"NazwaKlasy": klasa_old}
            values = {"$set": {"NazwaKlasy": klasa_new}}


            x = Klasy.update_one(location, values)


            Uczniowie.update_many(
                {"nr_klasy": klasa_old},
                {"$set": {"nr_klasy": klasa_new}}
            )


            Nauczyciele.update_many(
                {"NrKlasy": klasa_old},
                {"$set": {"NrKlasy": klasa_new}}
            )

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


def dropuczen(request, imie, nazwisko):
    if request.method == "POST":
        db = client['skibidi']
        kolekcja_klasy = db['Klasy']
        kolekcja_uczniow = db['Uczniowie']


        result_uczen = kolekcja_uczniow.delete_one({"Imie": imie, "Nazwisko": nazwisko})


        result_klasa = kolekcja_klasy.update_many(
            {"Uczniowie": {"$elemMatch": {"Imie": imie, "Nazwisko": nazwisko}}},
            {"$pull": {"Uczniowie": {"Imie": imie, "Nazwisko": nazwisko}}}
        )


        if result_uczen.deleted_count > 0:
            message = f"Uczeń {imie} {nazwisko} został usunięty."
        else:
            message = f"Nie znaleziono ucznia {imie} {nazwisko} w kolekcji uczniów."

        if result_klasa.modified_count > 0:
            message += " Uczeń został również usunięty z listy w klasach."
        else:
            message += " Nie znaleziono ucznia w żadnej klasie."

        return render(request, 'message.html', {"message": message})

    else:
        message = f"Czy na pewno chcesz usunąć ucznia {imie} {nazwisko}?"
        return render(request, 'usun_ucz.html', {"message": message})


def dropnauczyciel(request, imie, nazwisko):
    if request.method == "POST":
        db = client['skibidi']
        kolekcja_klasy = db['Klasy']
        kolekcja_nauczyciele = db['Nauczyciele']


        result_nauczyciel = kolekcja_nauczyciele.delete_one({"Imie": imie, "Nazwisko": nazwisko})


        result_klasa = kolekcja_klasy.update_many(
            {"Nauczyciele": {"$elemMatch": {"Imie": imie, "Nazwisko": nazwisko}}},
            {"$pull": {"Nauczyciele": {"Imie": imie, "Nazwisko": nazwisko}}}
        )


        if result_nauczyciel.deleted_count > 0:
            message = f"Nauczyciel {imie} {nazwisko} został usunięty."
        else:
            message = f"Nie znaleziono nauczyciela {imie} {nazwisko} w kolekcji nauczycieli."

        if result_klasa.modified_count > 0:
            message += " Nauczyciel został również usunięty z listy w klasach."
        else:
            message += " Nie znaleziono nauczyciela w żadnej klasie."

        return render(request, 'message.html', {"message": message})

    else:
        message = f"Czy na pewno chcesz usunąć nauczyciela {imie} {nazwisko}?"
        return render(request, 'usun_naucz.html', {"message": message})