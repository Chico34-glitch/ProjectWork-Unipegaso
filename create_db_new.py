import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, 'natural_belle.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crea tabella utenti
cursor.execute('''
CREATE TABLE IF NOT EXISTS utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    ruolo TEXT NOT NULL
)
''')

# Crea tabella appuntamenti
cursor.execute('''
CREATE TABLE IF NOT EXISTS appuntamenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    servizio TEXT NOT NULL,
    data TEXT NOT NULL,
    ora TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (cliente_id) REFERENCES utenti(id)
)
''')

conn.commit()
conn.close()

print("Database creato correttamente!")
