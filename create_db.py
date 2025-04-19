import sqlite3
import bcrypt

# Connessione al database
conn = sqlite3.connect('natural_belle.db')
cursor = conn.cursor()

# Creazione della tabella utenti
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    ruolo TEXT NOT NULL CHECK (ruolo IN ('cliente', 'dipendente'))
)
''')

# Creazione della tabella prenotazioni
cursor.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    servizio TEXT NOT NULL,
    data TEXT NOT NULL,
    ora TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (cliente_id) REFERENCES users(id)
)
''')

# Funzione per inserire un dipendente di esempio
def inserisci_dipendente(nome, email, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
    INSERT INTO users (nome, email, password_hash, ruolo)
    VALUES (?, ?, ?, 'dipendente')
    ''', (nome, email, password_hash.decode('utf-8')))
    conn.commit()

# Inserimento dipendente di esempio
try:
    inserisci_dipendente('Mario Rossi', 'mario.rossi@naturalbelle.it', 'password123')
    print("Dipendente inserito correttamente!")
except sqlite3.IntegrityError:
    print("Il dipendente esiste già, nessun inserimento effettuato.")

# Chiusura connessione
conn.close()
