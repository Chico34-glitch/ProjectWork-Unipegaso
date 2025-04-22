from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Percorso assoluto corretto al database
basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, 'natural_belle.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inizializzazione Flask
app = Flask(__name__)
CORS(app)

# Segreto per i token JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Rotta iniziale
@app.route('/')
def index():
    return render_template('login.html')

# Rotta di registrazione
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({"error": "Email già registrata"}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, ?)",
                   (email, hashed_password, "cliente"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Registrazione completata!"}), 201

# Rotta di login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={"id": user["id"], "ruolo": user["ruolo"]})
        return jsonify(access_token=access_token, ruolo=user["ruolo"])
    else:
        return jsonify({"error": "Email o password non validi"}), 401

# API prenotazione cliente
@app.route('/prenotazione', methods=['POST'])
@jwt_required()
def prenota_servizio():
    current_user = get_jwt_identity()

    data = request.get_json(force=True)
    servizio = data.get('servizio')
    data_prenotazione = data.get('data')
    ora = data.get('ora')
    note = data.get('note')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO appuntamenti (cliente_id, servizio, data, ora, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (current_user['id'], servizio, data_prenotazione, ora, note))

    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione registrata correttamente!"}), 201

# Test JSON - Nuova rotta
@app.route('/test_json', methods=['POST'])
def test_json():
    try:
        data = request.get_json(force=True)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Dashboard cliente
@app.route('/dashboard_cliente')
def dashboard_cliente():
    return render_template('dashboard_cliente.html')

# Dashboard dipendente
@app.route('/dashboard_dipendente')
def dashboard_dipendente():
    return render_template('dashboard_dipendente.html')

# Avvio applicazione
if __name__ == '__main__':
    app.run(debug=True)
