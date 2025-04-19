from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Cambiala in produzione!
jwt = JWTManager(app)

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect('natural_belle.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rotta per la home (login page)
@app.route('/')
def index():
    return render_template('login.html')

# Rotta per login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={"id": user['id'], "ruolo": user['ruolo']})
        return jsonify(access_token=access_token, ruolo=user['ruolo']), 200
    else:
        return jsonify({"error": "Credenziali non valide"}), 401

# Rotta per registrazione clienti
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"error": "Utente già esistente"}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, ?)", (email, hashed_password, "cliente"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Registrazione avvenuta con successo!"}), 201

# Rotta per creare una nuova prenotazione (solo clienti)
@app.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    identity = get_jwt_identity()
    if identity['ruolo'] != "cliente":
        return jsonify({"error": "Solo i clienti possono creare prenotazioni"}), 403

    data = request.get_json()
    servizio = data.get('servizio')
    data_servizio = data.get('data')
    ora_servizio = data.get('ora')
    note = data.get('note')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appuntamenti (cliente_id, servizio, data, ora, note) VALUES (?, ?, ?, ?, ?)",
                   (identity['id'], servizio, data_servizio, ora_servizio, note))
    conn.commit()
    conn.close()
    return jsonify({"message": "Prenotazione creata con successo!"}), 201

# Rotta per vedere tutte le proprie prenotazioni (clienti) o tutte (dipendenti)
@app.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    identity = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()

    if identity['ruolo'] == "cliente":
        cursor.execute("SELECT * FROM appuntamenti WHERE cliente_id = ?", (identity['id'],))
    else:  # dipendente
        cursor.execute("SELECT * FROM appuntamenti")

    appointments = cursor.fetchall()
    conn.close()

    appointments_list = []
    for app in appointments:
        appointments_list.append({
            "id": app['id'],
            "cliente_id": app['cliente_id'],
            "servizio": app['servizio'],
            "data": app['data'],
            "ora": app['ora'],
            "note": app['note']
        })

    return jsonify(appointments_list), 200

# Rotta per modificare una prenotazione
@app.route('/appointments/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    identity = get_jwt_identity()
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Se è cliente, può modificare solo le proprie prenotazioni
    if identity['ruolo'] == "cliente":
        cursor.execute("SELECT * FROM appuntamenti WHERE id = ? AND cliente_id = ?", (id, identity['id']))
    else:  # dipendente
        cursor.execute("SELECT * FROM appuntamenti WHERE id = ?", (id,))

    appointment = cursor.fetchone()

    if not appointment:
        conn.close()
        return jsonify({"error": "Prenotazione non trovata"}), 404

    cursor.execute("UPDATE appuntamenti SET servizio = ?, data = ?, ora = ?, note = ? WHERE id = ?",
                   (data['servizio'], data['data'], data['ora'], data['note'], id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione aggiornata con successo!"}), 200

# Rotta per cancellare una prenotazione
@app.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    identity = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Se è cliente, può cancellare solo le proprie prenotazioni
    if identity['ruolo'] == "cliente":
        cursor.execute("SELECT * FROM appuntamenti WHERE id = ? AND cliente_id = ?", (id, identity['id']))
    else:  # dipendente
        cursor.execute("SELECT * FROM appuntamenti WHERE id = ?", (id,))

    appointment = cursor.fetchone()

    if not appointment:
        conn.close()
        return jsonify({"error": "Prenotazione non trovata"}), 404

    cursor.execute("DELETE FROM appuntamenti WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione cancellata con successo!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
