# (Tutto l'app.py resta uguale fino a...)

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

@app.route('/prenotazioni_dipendenti', methods=['GET'])
@jwt_required()
def prenotazioni_dipendenti():
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
