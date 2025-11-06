import random
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from .models import Porada, Egzamin, Przesad

def index(request):
    """
    Prosta strona startowa z linkami do endpointow API.
    """
    return HttpResponse(
        "<h1>Asystent sesji – API</h1>"
        "<ul>"
        "<li><a href='/admin/'>/admin/</a></li>"
        "<li><a href='/api/porada/losowa/'>/api/porada/losowa/</a></li>"
        "<li><a href='/api/egzaminy/'>/api/egzaminy/</a></li>"
        "<li><a href='/api/przesady/?losowy=1'>/api/przesady/?losowy=1</a></li>"
        "</ul>"
    )

@require_GET
def api_losowa_porada(request):
    """
    Zwraca losowa porade motywacyjna w formacie JSON.
    """
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
    """
    Zwraca posortowana liste egzaminow; opcjonalny filtr: ?typ=pisemny
    """
    qs = Egzamin.objects.all()
    typ = request.GET.get('typ')
    if typ:
        qs = qs.filter(typ=typ)
    dane = [{
        "przedmiot": e.przedmiot,
        "data": e.data.isoformat(),
        "godzina": e.godzina.isoformat(timespec='minutes'),
        "miejsce": e.miejsce,
        "typ": e.typ
    } for e in qs.order_by('data', 'godzina')]
    return JsonResponse({"egzaminy": dane})

@require_GET
def api_przesady(request):
    """
    Zwraca liste przesadow lub losowy przesad (?losowy=1).
    """
    if request.GET.get('losowy') == '1':
        liczba = Przesad.objects.count()
        if liczba == 0:
            return JsonResponse({"przesad": None, "komunikat": "Brak przesadow w bazie."}, status=404)
        p = Przesad.objects.all()[random.randint(0, liczba - 1)]
        return JsonResponse({"przesad": {"tekst": p.tekst, "opis_pochodzenia": p.opis_pochodzenia}})
    lista = [{"tekst": p.tekst, "opis_pochodzenia": p.opis_pochodzenia} for p in Przesad.objects.all()]
    return JsonResponse({"przesady": lista})
