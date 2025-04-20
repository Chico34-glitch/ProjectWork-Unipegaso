import sqlite3
from werkzeug.security import generate_password_hash

# Connessione al nuovo database
conn = sqlite3.connect('natural_belle.db')
cursor = conn.cursor()

# Creazione tabella utenti
cursor.execute('''
CREATE TABLE IF NOT EXISTS utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    ruolo TEXT NOT NULL
)
''')

# Creazione tabella appuntamenti
cursor.execute('''
CREATE TABLE IF NOT EXISTS appuntamenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    servizio TEXT NOT NULL,
    data TEXT NOT NULL,
    ora TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (cliente_id) REFERENCES utenti (id)
)
''')

# Inserimento dipendente base
email_dipendente = "mario.rossi@naturalbelle.it"
password_dipendente = generate_password_hash("password123")
ruolo_dipendente = "dipendente"

cursor.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, ?)", 
               (email_dipendente, password_dipendente, ruolo_dipendente))

conn.commit()
conn.close()

print("Database creato e dipendente inserito!")
