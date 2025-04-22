from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3

app = Flask(__name__)  # <-- CORRETTO: __name__ con due underscore
CORS(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

# Connessione al DB
def get_db_connection():
    conn = sqlite3.connect('natural_belle.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home
@app.route('/')
def home():
    return render_template('login.html')

# Dashboard cliente
@app.route('/dashboard_cliente')
@jwt_required()
def dashboard_cliente():
    current_user = get_jwt_identity()
    if current_user['ruolo'] != 'cliente':
        return jsonify({"error": "Accesso non autorizzato"}), 403
    return render_template('dashboard_cliente.html')

# Dashboard dipendente
@app.route('/dashboard_dipendente')
@jwt_required()
def dashboard_dipendente():
    current_user = get_jwt_identity()
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403
    return render_template('dashboard_dipendente.html')

# Registrazione cliente
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email e password obbligatorie"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM utenti WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Email già registrata"}), 400

    cursor.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, 'cliente')", (email, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "Registrazione completata!"}), 201

# Login clienti/dipendenti
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        token = create_access_token(identity={
            'id': user['id'],
            'email': user['email'],
            'ruolo': user['ruolo']
        })
        return jsonify(access_token=token, ruolo=user['ruolo'])
    else:
        return jsonify({"error": "Email o password errati"}), 401

# Prenotazione
@app.route('/prenotazione', methods=['POST'])
@jwt_required()
def prenotazione():
    current_user = get_jwt_identity()
    cliente_id = current_user['id']

    data = request.get_json()
    servizio = data.get('servizio')
    data_servizio = data.get('data')
    ora = data.get('ora')
    note = data.get('note')

    if not servizio or not data_servizio or not ora:
        return jsonify({"error": "Tutti i campi tranne le note sono obbligatori"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appuntamenti (cliente_id, servizio, data, ora, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, servizio, data_servizio, ora, note))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione avvenuta con successo!"})

# Prenotazioni cliente
@app.route('/prenotazioni_cliente', methods=['GET'])
@jwt_required()
def prenotazioni_cliente():
    current_user = get_jwt_identity()
    cliente_id = current_user['id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT servizio, data, ora, note
        FROM appuntamenti
        WHERE cliente_id = ?
        ORDER BY data, ora
    ''', (cliente_id,))
    prenotazioni = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in prenotazioni])

# Prenotazioni per dipendenti
@app.route('/prenotazioni_dipendenti', methods=['GET'])
@jwt_required()
def prenotazioni_dipendenti():
    current_user = get_jwt_identity()
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT utenti.email, appuntamenti.servizio, appuntamenti.data, appuntamenti.ora, appuntamenti.note
        FROM appuntamenti
        JOIN utenti ON appuntamenti.cliente_id = utenti.id
        ORDER BY appuntamenti.data, appuntamenti.ora
    ''')
    prenotazioni = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in prenotazioni])

# Avvio server
if __name__ == '__main__':
    app.run(debug=True)
