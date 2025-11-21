from django import forms
from .models import Egzamin


class EgzaminForm(forms.ModelForm):
    """Formularz do dodawania egzaminów przez użytkownika."""

    class Meta:
        model = Egzamin
        fields = ["przedmiot", "data", "godzina", "miejsce", "typ"]
        labels = {
            "przedmiot": "Przedmiot",
            "data": "Data egzaminu",
            "godzina": "Godzina",
            "miejsce": "Miejsce",
            "typ": "Typ egzaminu",
        }
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "godzina": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "przedmiot": forms.TextInput(attrs={"class": "form-control"}),
            "miejsce": forms.TextInput(attrs={"class": "form-control"}),
            "typ": forms.Select(attrs={"class": "form-select"}),
        }
