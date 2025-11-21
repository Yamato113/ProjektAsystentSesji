import random
import csv

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Porada, Egzamin, Przesad
from .forms import EgzaminForm


def index(request):
    """Strona glówna aplikacji."""
    return render(request, "main/index.html")


def kalendarz(request):
    """
    Widok kalendarza egzaminów:
    - wyswietla liste egzaminów z bazy, posortowaną rosnąco po dacie i godzinie,
    - pozwala dodawac nowe egzaminy przez ModelForm,
    - opcjonalnie filtruje po typie (?typ=pisemny / ustny / projekt).
    """

    # --- filtrowanie (funkcja dodatkowa z punktu C) ---
    typ_filtru = request.GET.get("typ")
    if typ_filtru:
        egzaminy = Egzamin.objects.filter(typ=typ_filtru).order_by("data", "godzina")
    else:
        egzaminy = Egzamin.objects.all().order_by("data", "godzina")

    # --- obsluga formularza dodawania egzaminu ---
    if request.method == "POST":
        form = EgzaminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("kalendarz"))
    else:
        form = EgzaminForm()

    return render(
        request,
        "main/kalendarz.html",
        {
            "egzaminy": egzaminy,
            "form": form,
            "typ_filtru": typ_filtru or "",
        }
    )


def przesady_strona(request):
    """
    Widok przesądów:
    - pokazuje liste przesądów z bazy,
    - obsluguje losowanie przez parametr GET (?losowy=1).
    """
    przesady = list(Przesad.objects.all())
    losowy_param = request.GET.get("losowy")

    przesad_losowy = None
    if losowy_param and przesady:
        przesad_losowy = random.choice(przesady)

    return render(
        request,
        "main/przesady.html",
        {
            "przesady": przesady,
            "przesad_losowy": przesad_losowy,
        }
    )


def export_egzaminy_csv(request):
    """Eksportuje liste egzaminów do pliku CSV (funkcja dodatkowa)."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="egzaminy.csv"'

    writer = csv.writer(response)
    writer.writerow(["Przedmiot", "Data", "Godzina", "Miejsce", "Typ"])

    for e in Egzamin.objects.all().order_by("data", "godzina"):
        writer.writerow([e.przedmiot, e.data, e.godzina, e.miejsce, e.typ])

    return response


@require_GET
def api_losowa_porada(request):
    liczba = Porada.objects.count()
    if liczba == 0:
        return JsonResponse({"porada": None, "komunikat": "Brak porad w bazie."}, status=404)
    indeks = random.randint(0, liczba - 1)
    porada = Porada.objects.all()[indeks]
    return JsonResponse({
        "porada": {"tekst": porada.tekst, "kategoria": porada.kategoria}
    })


@require_GET
def api_lista_egzaminow(request):
    qs = Egzamin.objects.all()
    typ = request.GET.get("typ")
    if typ:
        qs = qs.filter(typ=typ)

    dane = [{
        "przedmiot": e.przedmiot,
        "data": e.data.isoformat(),
        "godzina": e.godzina.isoformat(timespec="minutes"),
        "miejsce": e.miejsce,
        "typ": e.typ
    } for e in qs.order_by("data", "godzina")]

    return JsonResponse({"egzaminy": dane})


@require_GET
def api_przesady(request):
    if request.GET.get("losowy") == "1":
        liczba = Przesad.objects.count()
        if liczba == 0:
            return JsonResponse({"przesad": None, "komunikat": "Brak przesadow w bazie."}, status=404)
        p = Przesad.objects.all()[random.randint(0, liczba - 1)]
        return JsonResponse({"przesad": {"tekst": p.tekst, "opis_pochodzenia": p.opis_pochodzenia}})

    lista = [{"tekst": p.tekst, "opis_pochodzenia": p.opis_pochodzenia} for p in Przesad.objects.all()]
    return JsonResponse({"przesady": lista})
