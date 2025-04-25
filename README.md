## Come iniziare

### 1. Installazione delle dipendenze
Assicurati di avere **Python 3.9+** installato. Apri il terminale e installa le librerie necessarie:

```bash
pip install flask flask-cors flask-jwt-extended
```

---

### 2. Creazione del database

Per generare il database SQLite (`natural_belle.db`) esegui:

```bash
python create_db_new.py
python create_dipendente.py
```

Questo:
- Crea il file `natural_belle.db`
- Genera automaticamente le tabelle `utenti` e `appuntamenti`
- Credenziali dipendenti:
  - **Email**: `dipendente@naturalbelle.it`
  - **Password**: `admin123`

> **Nota**: Il database non è incluso nel repository GitHub per motivi di sicurezza. Va generato localmente con i file sopra.

---

### 3. Avvio dell'applicazione

Per avviare il server Flask, esegui da terminale:

```bash
python app.py
```

Visita poi l'applicazione nel browser all’indirizzo:

```
http://127.0.0.1:5000
```

---

## Funzionalità principali

- **Registrazione e login cliente**
- **Login dipendente preconfigurato**
- **Prenotazione con selezione servizio, data, ora, note**
- **Visualizzazione prenotazioni cliente**
- **Visualizzazione, modifica e cancellazione prenotazioni da parte del dipendente**
- **Gestione sicura tramite token JWT**
- **Persistenza dei dati con SQLite**
- **Front-end responsivo e dinamico**
