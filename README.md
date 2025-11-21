Projekt zostal wykonany.

Autorzy poszczegolnych czesci:
- Część A: Yaroslav Velychko
- Część B: Vladyslav Yakovlev
- Część C: Denys Lopatskyi

Aby uruchomic program, wykonaj ponizsze kroki:

Wejdz do katalogu projektu:
cd asystent_sesji

Utworz wirtualne srodowisko:
Windows:
python -m venv venv
Linux/macOS:
python3 -m venv venv

Aktywuj wirtualne srodowisko:
Windows (PowerShell):
venv\Scripts\Activate.ps1
Windows (CMD):
venv\Scripts\activate
Linux/macOS:
source venv/bin/activate

Zainstaluj wymagane pakiety:
pip install -r requirements.txt
Jesli plik requirements.txt nie istnieje:
pip install django

Wykonaj migracje bazy danych:
python manage.py makemigrations
python manage.py migrate

Uruchom serwer aplikacji:
python manage.py runserver

Nastepnie otworz w przegladarce adres:
http://127.0.0.1:8000/
