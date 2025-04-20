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
    data = request.get_json()
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
    data = request.get_json()
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

# Dashboard cliente
@app.route('/dashboard_cliente')
@jwt_required()
def dashboard_cliente():
    current_user = get_jwt_identity()
    if current_user["ruolo"] != "cliente":
        return jsonify({"error": "Accesso negato"}), 403
    return render_template('dashboard_cliente.html')

# Dashboard dipendente
@app.route('/dashboard_dipendente')
@jwt_required()
def dashboard_dipendente():
    current_user = get_jwt_identity()
    if current_user["ruolo"] != "dipendente":
        return jsonify({"error": "Accesso negato"}), 403
    return render_template('dashboard_dipendente.html')

# Avvio applicazione
if __name__ == '__main__':
    app.run(debug=True)
