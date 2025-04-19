from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import bcrypt

# Inizializza Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key-naturalbelle'
jwt = JWTManager(app)

# Connessione database
def get_db_connection():
    conn = sqlite3.connect('natural_belle.db')
    conn.row_factory = sqlite3.Row
    return conn

# Homepage → Login page
@app.route('/')
def home():
    return render_template('login.html')

# Registrazione clienti
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')

    if not nome or not email or not password:
        return jsonify({"error": "Tutti i campi sono obbligatori!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Email già registrata."}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('''
    INSERT INTO users (nome, email, password_hash, ruolo)
    VALUES (?, ?, ?, 'cliente')
    ''', (nome, email, password_hash.decode('utf-8')))
    conn.commit()
    conn.close()

    return jsonify({"message": "Registrazione avvenuta con successo!"}), 201

# Login clienti/dipendenti
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        access_token = create_access_token(identity={'id': user['id'], 'ruolo': user['ruolo'], 'nome': user['nome']})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenziali non valide."}), 401

# Dashboard clienti
@app.route('/dashboard_cliente')
@jwt_required()
def dashboard_cliente():
    return "Benvenuto nella dashboard cliente!"

# Dashboard dipendenti
@app.route('/dashboard_dipendente')
@jwt_required()
def dashboard_dipendente():
    return "Benvenuto nella dashboard dipendente!"

# Creazione prenotazione
@app.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    current_user = get_jwt_identity()

    if current_user['ruolo'] != 'cliente':
        return jsonify({"error": "Solo i clienti possono creare prenotazioni."}), 403

    data = request.get_json()
    servizio = data.get('servizio')
    data_appuntamento = data.get('data')
    ora_appuntamento = data.get('ora')
    note = data.get('note', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (cliente_id, servizio, data, ora, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (current_user['id'], servizio, data_appuntamento, ora_appuntamento, note))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione creata con successo!"}), 201

# Visualizzazione prenotazioni
@app.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()

    if current_user['ruolo'] == 'cliente':
        cursor.execute('SELECT * FROM appointments WHERE cliente_id = ?', (current_user['id'],))
    else:
        cursor.execute('SELECT * FROM appointments')

    appointments = cursor.fetchall()
    conn.close()

    return jsonify([dict(appointment) for appointment in appointments]), 200

if __name__ == '__main__':
    app.run(debug=True)
