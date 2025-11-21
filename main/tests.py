from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Porada, Egzamin, Przesad


class TestyModeli(TestCase):
    """Testy podstawowych modeli aplikacji."""

    def test_str_porada(self):
        p = Porada.objects.create(
            tekst="Testowa porada motywacyjna",
            kategoria="motywacja"
        )
        s = str(p)
        self.assertIn("motywacja", s)
        self.assertIn("Testowa porada", s)

    def test_str_egzamin(self):
        e = Egzamin.objects.create(
            przedmiot="Matematyka",
            data=date(2025, 1, 20),
            godzina=time(9, 30),
            miejsce="Sala 101",
            typ="pisemny"
        )
        s = str(e)
        self.assertIn("Matematyka", s)
        self.assertIn("2025-01-20", s)

    def test_str_przesad(self):
        pr = Przesad.objects.create(
            tekst="Nie obcinaj wlosow przed egzaminem!",
            opis_pochodzenia="Tradycja studencka"
        )
        self.assertEqual(str(pr), "Nie obcinaj wlosow przed egzaminem!")

    def test_kolejnosc_egzaminow(self):
        """Sprawdza sortowanie egzaminów po dacie i godzinie (Meta.ordering)."""
        Egzamin.objects.create(
            przedmiot="Fizyka",
            data=date(2025, 2, 5),
            godzina=time(12, 0),
            miejsce="A1",
            typ="ustny"
        )
        Egzamin.objects.create(
            przedmiot="Chemia",
            data=date(2025, 1, 25),
            godzina=time(8, 0),
            miejsce="B2",
            typ="pisemny"
        )
        Egzamin.objects.create(
            przedmiot="Biologia",
            data=date(2025, 1, 25),
            godzina=time(7, 30),
            miejsce="C3",
            typ="pisemny"
        )

        qs = list(Egzamin.objects.all())
        self.assertEqual(qs[0].przedmiot, "Biologia")
        self.assertEqual(qs[1].przedmiot, "Chemia")
        self.assertEqual(qs[2].przedmiot, "Fizyka")


class TestyApiPorad(TestCase):
    """Testy endpointu losowej porady."""

    def test_losowa_porada_gdy_pusto(self):
        url = reverse("api_losowa_porada")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)

        data_json = r.json()
        self.assertIn("porada", data_json)
        self.assertIsNone(data_json["porada"])
        self.assertIn("komunikat", data_json)

    def test_losowa_porada_gdy_sa_dane(self):
        Porada.objects.create(tekst="Testowa porada", kategoria="motywacja")
        Porada.objects.create(tekst="Druga porada", kategoria="nauka")

        url = reverse("api_losowa_porada")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        data_json = r.json()
        self.assertIn("porada", data_json)
        self.assertIn("tekst", data_json["porada"])
        self.assertIn("kategoria", data_json["porada"])
        self.assertIn(data_json["porada"]["tekst"], ["Testowa porada", "Druga porada"])


class TestyApiEgzaminow(TestCase):
    """Testy listy egzaminów + filtrowanie po typie."""

    def setUp(self):
        Egzamin.objects.create(
            przedmiot="Analiza",
            data=date(2025, 1, 10),
            godzina=time(10, 0),
            miejsce="S1",
            typ="pisemny"
        )
        Egzamin.objects.create(
            przedmiot="Programowanie",
            data=date(2025, 1, 12),
            godzina=time(9, 0),
            miejsce="S2",
            typ="projekt"
        )
        Egzamin.objects.create(
            przedmiot="Algebra",
            data=date(2025, 1, 12),
            godzina=time(8, 30),
            miejsce="S3",
            typ="pisemny"
        )

    def test_lista_egzaminow_format_i_sortowanie(self):
        url = reverse("api_lista_egzaminow")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        data_json = r.json()
        self.assertIn("egzaminy", data_json)
        egzaminy = data_json["egzaminy"]
        self.assertEqual(len(egzaminy), 3)

        # sortowanie: data rosnąco, potem godzina
        self.assertEqual(egzaminy[0]["przedmiot"], "Analiza")
        self.assertEqual(egzaminy[1]["przedmiot"], "Algebra")
        self.assertEqual(egzaminy[2]["przedmiot"], "Programowanie")

        # formaty pól
        self.assertRegex(egzaminy[0]["data"], r"\d{4}-\d{2}-\d{2}")
        self.assertRegex(egzaminy[0]["godzina"], r"\d{2}:\d{2}")

    def test_filtrowanie_po_typie(self):
        url = reverse("api_lista_egzaminow")

        r = self.client.get(url, {"typ": "pisemny"})
        self.assertEqual(r.status_code, 200)
        egzaminy = r.json()["egzaminy"]

        self.assertEqual(len(egzaminy), 2)
        self.assertTrue(all(e["typ"] == "pisemny" for e in egzaminy))


class TestyApiPrzesadow(TestCase):
    """Testy listy przesądów i endpointu losowego przesądu."""

    def test_przesady_lista_gdy_pusto(self):
        url = reverse("api_przesady")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        data_json = r.json()
        self.assertIn("przesady", data_json)
        self.assertEqual(data_json["przesady"], [])

    def test_przesad_losowy_gdy_pusto(self):
        url = reverse("api_przesady")
        r = self.client.get(url, {"losowy": "1"})
        self.assertEqual(r.status_code, 404)

        data_json = r.json()
        self.assertIn("przesad", data_json)
        self.assertIsNone(data_json["przesad"])
        self.assertIn("komunikat", data_json)

    def test_przesady_lista_i_losowy_gdy_sa_dane(self):
        Przesad.objects.create(tekst="Czerwone majtki na szczescie", opis_pochodzenia="")
        Przesad.objects.create(tekst="Nie myj glowy przed egzaminem", opis_pochodzenia="")

        url = reverse("api_przesady")

        r_lista = self.client.get(url)
        self.assertEqual(r_lista.status_code, 200)
        self.assertEqual(len(r_lista.json()["przesady"]), 2)

        r_losowy = self.client.get(url, {"losowy": "1"})
        self.assertEqual(r_losowy.status_code, 200)

        przesad = r_losowy.json()["przesad"]
        self.assertIn("tekst", przesad)
        self.assertIn(przesad["tekst"], [
            "Czerwone majtki na szczescie",
            "Nie myj glowy przed egzaminem"
        ])
