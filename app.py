from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3

app = Flask(_name_)
CORS(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

# Funzione di connessione al database
def get_db_connection():
    conn = sqlite3.connect('natural_belle.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page (Login e Registrazione)
@app.route('/')
def home():
    return render_template('login.html')

# Dashboard Cliente
@app.route('/dashboard_cliente')
@jwt_required()
def dashboard_cliente():
    current_user = get_jwt_identity()
    if current_user['ruolo'] != 'cliente':
        return jsonify({"error": "Accesso non autorizzato"}), 403
    return render_template('dashboard_cliente.html')

# Dashboard Dipendente
@app.route('/dashboard_dipendente')
@jwt_required()
def dashboard_dipendente():
    current_user = get_jwt_identity()
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403
    return render_template('dashboard_dipendente.html')

# Registrazione nuovo cliente
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
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"error": "Email già registrata"}), 400

    cursor.execute("INSERT INTO utenti (email, password, ruolo) VALUES (?, ?, 'cliente')", (email, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "Registrazione completata!"}), 201

# Login clienti e dipendenti
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
        access_token = create_access_token(identity={
            'id': user['id'],
            'email': user['email'],
            'ruolo': user['ruolo']
        })
        return jsonify(access_token=access_token, ruolo=user['ruolo'])
    else:
        return jsonify({"error": "Email o password errate"}), 401

# Prenotazione di un servizio da parte del cliente
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
        return jsonify({"error": "Tutti i campi tranne le note sono obbligatori."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO appuntamenti (cliente_id, servizio, data, ora, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, servizio, data_servizio, ora, note))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione avvenuta con successo!"})

# Recupera prenotazioni del cliente loggato
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

    results = [dict(row) for row in prenotazioni]
    return jsonify(results)

# Recupera tutte le prenotazioni per i dipendenti
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

    results = [dict(row) for row in prenotazioni]
    return jsonify(results)

# Avvio applicazione
if _name_ == '_main_':
    app.run(debug=True)
