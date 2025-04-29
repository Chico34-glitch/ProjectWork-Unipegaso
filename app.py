from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

def get_db_connection():
    conn = sqlite3.connect('natural_belle.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route('/')
def home():
    return render_template('login.html')

# Dashboard Cliente
@app.route('/dashboard_cliente')
def dashboard_cliente():
    return render_template('dashboard_cliente.html')

# Dashboard Dipendente
@app.route('/dashboard_dipendente')
def dashboard_dipendente():
    return render_template('dashboard_dipendente.html')

# Registrazione
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

# Login
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
        user_identity = json.dumps({
            'id': user['id'],
            'email': user['email'],
            'ruolo': user['ruolo']
        })
        token = create_access_token(identity=user_identity)
        return jsonify(access_token=token, ruolo=user['ruolo'])
    else:
        return jsonify({"error": "Email o password errati"}), 401

# Prenotazione Cliente (POST su /prenotazioni)
@app.route('/prenotazioni', methods=['POST'])
@jwt_required()
def crea_prenotazione():
    current_user = json.loads(get_jwt_identity())
    cliente_id = current_user['id']

    data = request.get_json(force=True)
    servizio = data.get('servizio')
    data_servizio = data.get('data')
    ora = data.get('ora')
    note = data.get('note', '')

    if not servizio or not data_servizio or not ora:
        return jsonify({"error": "Tutti i campi obbligatori devono essere compilati"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appuntamenti (cliente_id, servizio, data, ora, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, servizio, data_servizio, ora, note))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione avvenuta con successo!"}), 201

# Visualizza prenotazioni Cliente
@app.route('/prenotazioni_cliente', methods=['GET'])
@jwt_required()
def prenotazioni_cliente():
    current_user = json.loads(get_jwt_identity())
    cliente_id = current_user['id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, servizio, data, ora, note
        FROM appuntamenti
        WHERE cliente_id = ?
        ORDER BY data, ora
    ''', (cliente_id,))
    prenotazioni = cursor.fetchall()
    conn.close()

    results = [dict(p) for p in prenotazioni]
    return jsonify(results)

# Visualizza prenotazioni Dipendente
@app.route('/prenotazioni', methods=['GET'])
@jwt_required()
def prenotazioni():
    current_user = json.loads(get_jwt_identity())
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT appuntamenti.id, servizio, data, ora, note, utenti.email as cliente_email
        FROM appuntamenti
        JOIN utenti ON appuntamenti.cliente_id = utenti.id
        ORDER BY data, ora
    ''')
    prenotazioni = cursor.fetchall()
    conn.close()

    results = [dict(p) for p in prenotazioni]
    return jsonify(results)

# Modifica prenotazione Dipendente
@app.route('/modifica_prenotazione/<int:id>', methods=['PUT'])
@jwt_required()
def modifica_prenotazione(id):
    current_user = json.loads(get_jwt_identity())
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403

    data = request.get_json()
    servizio = data.get('servizio')
    data_servizio = data.get('data')
    ora = data.get('ora')
    note = data.get('note')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE appuntamenti
        SET servizio = ?, data = ?, ora = ?, note = ?
        WHERE id = ?
    ''', (servizio, data_servizio, ora, note, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione modificata con successo!"})

# Cancella prenotazione Dipendente
@app.route('/cancella_prenotazione/<int:id>', methods=['DELETE'])
@jwt_required()
def cancella_prenotazione(id):
    current_user = json.loads(get_jwt_identity())
    if current_user['ruolo'] != 'dipendente':
        return jsonify({"error": "Accesso non autorizzato"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appuntamenti WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione cancellata con successo!"})

# Modifica prenotazione Cliente (AGGIORNATO)
@app.route('/modifica_prenotazione_cliente/<int:id>', methods=['PUT'])
@jwt_required()
def modifica_prenotazione_cliente(id):
    current_user = json.loads(get_jwt_identity())
    cliente_id = current_user['id']

    data = request.get_json()
    nuovo_servizio = data.get('servizio')
    nuova_data = data.get('data')
    nuova_ora = data.get('ora')
    nuove_note = data.get('note', '')

    if not nuovo_servizio or not nuova_data or not nuova_ora:
        return jsonify({"error": "Dati mancanti"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE appuntamenti
        SET servizio = ?, data = ?, ora = ?, note = ?
        WHERE id = ? AND cliente_id = ?
    ''', (nuovo_servizio, nuova_data, nuova_ora, nuove_note, id, cliente_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione modificata con successo!"})

# Cancella prenotazione Cliente
@app.route('/cancella_prenotazione_cliente/<int:id>', methods=['DELETE'])
@jwt_required()
def cancella_prenotazione_cliente(id):
    current_user = json.loads(get_jwt_identity())
    cliente_id = current_user['id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appuntamenti WHERE id = ? AND cliente_id = ?', (id, cliente_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione cancellata con successo!"})

if __name__ == '__main__':
    app.run(debug=True)
