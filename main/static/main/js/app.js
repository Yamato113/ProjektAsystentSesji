document.addEventListener('DOMContentLoaded', () => {
    // Strona glowna: losowa porada
    const btnPorada = document.getElementById('btn-porada');
    if (btnPorada) {
        btnPorada.addEventListener('click', () => {
            pobierzLosowaPorade();
        });
    }

    // Strona kalendarza egzaminow
    const tabelaEgzaminow = document.getElementById('tabela-egzaminow');
    if (tabelaEgzaminow) {
        const selectTyp = document.getElementById('typ-egzaminu');
        // Zaladuj wszystkie egzaminy przy starcie
        pobierzEgzaminy('');

        if (selectTyp) {
            selectTyp.addEventListener('change', () => {
                const wybranyTyp = selectTyp.value;
                pobierzEgzaminy(wybranyTyp);
            });
        }
    }

    // Strona przesadow
    const btnLosujPrzesad = document.getElementById('btn-losuj-przesad');
    const btnWszystkiePrzesady = document.getElementById('btn-wszystkie-przesady');

    if (btnLosujPrzesad) {
        btnLosujPrzesad.addEventListener('click', () => {
            pobierzLosowyPrzesad();
        });
    }

    if (btnWszystkiePrzesady) {
        btnWszystkiePrzesady.addEventListener('click', () => {
            pobierzWszystkiePrzesady();
        });
    }
});

// === PORADY ===

function pobierzLosowaPorade() {
    const wynikDiv = document.getElementById('porada-wynik');
    if (!wynikDiv) return;

    wynikDiv.innerHTML = '<p>Ładowanie porady...</p>';

    fetch('/api/porada/losowa/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania porady');
            }
            return response.json();
        })
        .then(data => {
            if (!data.porada) {
                wynikDiv.innerHTML = `<p>${data.komunikat || 'Brak porad w bazie.'}</p>`;
                return;
            }
            const tekst = data.porada.tekst;
            const kategoria = data.porada.kategoria;

            wynikDiv.innerHTML = `
                <p><strong>Kategoria:</strong> ${kategoria}</p>
                <p>${tekst}</p>
            `;
        })
        .catch(error => {
            console.error(error);
            wynikDiv.innerHTML = '<p>Wystąpił błąd podczas pobierania porady.</p>';
        });
}


// === EGZAMINY ===

function pobierzEgzaminy(typ) {
    const tbody = document.querySelector('#tabela-egzaminow tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="5">Ładowanie egzaminów...</td></tr>';

    let url = '/api/egzaminy/';
    if (typ) {
        url += `?typ=${encodeURIComponent(typ)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania egzaminów');
            }
            return response.json();
        })
        .then(data => {
            const egzaminy = data.egzaminy || [];
            if (egzaminy.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5">Brak egzaminów do wyświetlenia.</td></tr>';
                return;
            }

            tbody.innerHTML = '';

            egzaminy.forEach(e => {
                const tr = document.createElement('tr');

                const tdPrzedmiot = document.createElement('td');
                tdPrzedmiot.textContent = e.przedmiot;

                const tdData = document.createElement('td');
                tdData.textContent = e.data;

                const tdGodzina = document.createElement('td');
                tdGodzina.textContent = e.godzina;

                const tdMiejsce = document.createElement('td');
                tdMiejsce.textContent = e.miejsce;

                const tdTyp = document.createElement('td');
                tdTyp.textContent = e.typ;

                tr.appendChild(tdPrzedmiot);
                tr.appendChild(tdData);
                tr.appendChild(tdGodzina);
                tr.appendChild(tdMiejsce);
                tr.appendChild(tdTyp);

                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error(error);
            tbody.innerHTML = '<tr><td colspan="5">Wystąpił błąd podczas pobierania egzaminów.</td></tr>';
        });
}


// === PRZESADY ===

function pobierzLosowyPrzesad() {
    const wynikDiv = document.getElementById('przesad-wynik');
    if (!wynikDiv) return;

    wynikDiv.innerHTML = '<p>Losowanie przesądu...</p>';

    fetch('/api/przesady/?losowy=1')
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania przesądu');
            }
            return response.json();
        })
        .then(data => {
            if (!data.przesad) {
                wynikDiv.innerHTML = `<p>${data.komunikat || 'Brak przesądów w bazie.'}</p>`;
                return;
            }
            const tekst = data.przesad.tekst;
            const opis = data.przesad.opis_pochodzenia || '';

            wynikDiv.innerHTML = `
                <p><strong>Przesąd:</strong> ${tekst}</p>
                <p><em>${opis}</em></p>
            `;
        })
        .catch(error => {
            console.error(error);
            wynikDiv.innerHTML = '<p>Wystąpił błąd podczas pobierania przesądu.</p>';
        });
}

function pobierzWszystkiePrzesady() {
    const lista = document.getElementById('lista-przesadow');
    const btn = document.getElementById('btn-wszystkie-przesady');

    if (!lista || !btn) return;

    // Jeśli lista jest już widoczna — ukryj ją
    if (!lista.classList.contains('hidden')) {
        lista.classList.add('hidden');
        btn.textContent = 'Pokaż wszystkie przesądy';
        return;
    }

    // W przeciwnym wypadku — pokaż i załaduj przesądy
    lista.classList.remove('hidden');
    lista.innerHTML = '<li>Ładowanie przesądów...</li>';
    btn.textContent = 'Ukryj przesądy';

    fetch('/api/przesady/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania przesądów');
            }
            return response.json();
        })
        .then(data => {
            const przesady = data.przesady || [];
            if (przesady.length === 0) {
                lista.innerHTML = '<li>Brak przesądów w bazie.</li>';
                return;
            }

            lista.innerHTML = '';

            przesady.forEach(p => {
                const li = document.createElement('li');
                const opis = p.opis_pochodzenia ? ` – ${p.opis_pochodzenia}` : '';
                li.textContent = `${p.tekst}${opis}`;
                lista.appendChild(li);
            });
        })
        .catch(error => {
            console.error(error);
            lista.innerHTML = '<li>Wystąpił błąd podczas pobierania przesądów.</li>';
        });
}
