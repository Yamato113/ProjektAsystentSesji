from django.contrib import admin
from .models import Egzamin, Porada, Przesad

@admin.register(Egzamin)
class EgzaminAdmin(admin.ModelAdmin):
    list_display = ('przedmiot', 'data', 'godzina', 'miejsce', 'typ')
    list_filter = ('typ', 'data')
    search_fields = ('przedmiot', 'miejsce')
    date_hierarchy = 'data'
    ordering = ('data', 'godzina')

@admin.register(Porada)
class PoradaAdmin(admin.ModelAdmin):
    list_display = ('kategoria', 'podglad')
    list_filter = ('kategoria',)
    search_fields = ('tekst',)

    def podglad(self, obj):
        return (obj.tekst[:60] + '...') if len(obj.tekst) > 60 else obj.tekst
    podglad.short_description = "Tekst (skrot)"

@admin.register(Przesad)
class PrzesadAdmin(admin.ModelAdmin):
    list_display = ('tekst',)
    search_fields = ('tekst', 'opis_pochodzenia')
