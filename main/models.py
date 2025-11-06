from django.db import models

class Egzamin(models.Model):
    """
    Model egzaminu — podstawowe informacje o terminach w sesji.
    """
    TYPY = [
        ('pisemny', 'Pisemny'),
        ('ustny', 'Ustny'),
        ('projekt', 'Projekt'),
        ('inne', 'Inne'),
    ]
    przedmiot = models.CharField(max_length=120, help_text="Nazwa przedmiotu")
    data = models.DateField(help_text="Data egzaminu")
    godzina = models.TimeField(help_text="Godzina egzaminu")
    miejsce = models.CharField(max_length=120, help_text="Sala lub budynek")
    typ = models.CharField(max_length=20, choices=TYPY, default='pisemny')

    class Meta:
        ordering = ['data', 'godzina']
        verbose_name = "Egzamin"
        verbose_name_plural = "Egzaminy"
        indexes = [
            models.Index(fields=['data', 'godzina']),
            models.Index(fields=['typ']),
        ]

    def __str__(self):
        return f"{self.przedmiot} — {self.data} {self.godzina} ({self.typ})"


class Porada(models.Model):
    """
    Porada motywacyjna dla studentow.
    """
    KATEGORIE = [
        ('motywacja', 'Motywacja'),
        ('nauka', 'Nauka'),
        ('zdrowie', 'Zdrowie'),
        ('inne', 'Inne'),
    ]
    tekst = models.TextField(help_text="Tresc porady")
    kategoria = models.CharField(max_length=20, choices=KATEGORIE, default='motywacja')

    class Meta:
        verbose_name = "Porada"
        verbose_name_plural = "Porady"
        indexes = [models.Index(fields=['kategoria'])]

    def __str__(self):
        return f"[{self.kategoria}] {self.tekst[:40]}..."


class Przesad(models.Model):
    """
    Studencki przesad z krotkim opisem pochodzenia.
    """
    tekst = models.CharField(max_length=180, help_text="Przesad — krotki tekst")
    opis_pochodzenia = models.TextField(blank=True, help_text="Skad sie wzial przesad (opcjonalnie)")

    class Meta:
        verbose_name = "Przesad"
        verbose_name_plural = "Przesady"

    def __str__(self):
        return self.tekst
