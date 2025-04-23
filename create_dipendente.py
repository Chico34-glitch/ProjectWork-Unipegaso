import sqlite3

# Connessione al database
conn = sqlite3.connect('natural_belle.db')
cursor = conn.cursor()

# Dati del dipendente
email = "dipendente@naturalbelle.it"
password = "admin123"
ruolo = "dipendente"

# Verifica se esiste già
cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
esiste = cursor.fetchone()

if esiste:
    print("⚠️ Il dipendente esiste già, nessuna modifica effettuata.")
else:
    # Inserimento nuovo dipendente
    cursor.execute("""
        INSERT INTO utenti (email, password, ruolo)
        VALUES (?, ?, ?)
    """, (email, password, ruolo))
    conn.commit()
    print("✅ Dipendente creato con successo!")

conn.close()
