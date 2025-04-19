document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    };

    // Funzione per caricare le prenotazioni
    const loadAppointments = async () => {
        const res = await fetch('/appointments', {
            headers
        });
        const appointments = await res.json();

        const list = document.getElementById('appointments-list');
        list.innerHTML = '';

        appointments.forEach(app => {
            const item = document.createElement('li');
            item.innerHTML = `
                <strong>${app.servizio}</strong><br>
                Data: ${app.data} - Ora: ${app.ora}<br>
                Note: ${app.note || 'Nessuna'}<br>
                <button onclick="showEditForm(${app.id})">Modifica</button>
                <button onclick="deleteAppointment(${app.id})">Cancella</button>
                <div id="edit-form-${app.id}" style="display:none;">
                    <input type="text" id="edit-servizio-${app.id}" placeholder="Servizio" value="${app.servizio}"><br>
                    <input type="date" id="edit-data-${app.id}" value="${app.data}"><br>
                    <input type="time" id="edit-ora-${app.id}" value="${app.ora}"><br>
                    <textarea id="edit-note-${app.id}" placeholder="Note">${app.note || ''}</textarea><br>
                    <button onclick="submitEdit(${app.id})">Salva Modifiche</button>
                </div>
                <hr>
            `;
            list.appendChild(item);
        });
    };

    // Creazione nuova prenotazione
    document.getElementById('new-appointment-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const servizio = document.getElementById('servizio').value;
        const data = document.getElementById('data').value;
        const ora = document.getElementById('ora').value;
        const note = document.getElementById('note').value;

        const body = { servizio, data, ora, note };

        const res = await fetch('/appointments', {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });

        const response = await res.json();

        if (res.ok) {
            document.getElementById('message').textContent = response.message;
            document.getElementById('error-message').textContent = '';
            document.getElementById('new-appointment-form').reset();
            loadAppointments();
        } else {
            document.getElementById('error-message').textContent = response.error;
            document.getElementById('message').textContent = '';
        }
    });

    // Mostra form di modifica
    window.showEditForm = (id) => {
        const form = document.getElementById(`edit-form-${id}`);
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    };

    // Invia modifiche
    window.submitEdit = async (id) => {
        const servizio = document.getElementById(`edit-servizio-${id}`).value;
        const data = document.getElementById(`edit-data-${id}`).value;
        const ora = document.getElementById(`edit-ora-${id}`).value;
        const note = document.getElementById(`edit-note-${id}`).value;

        const body = { servizio, data, ora, note };

        const res = await fetch(`/appointments/${id}`, {
            method: 'PUT',
            headers,
            body: JSON.stringify(body)
        });

        const response = await res.json();

        if (res.ok) {
            document.getElementById('message').textContent = response.message;
            document.getElementById('error-message').textContent = '';
            loadAppointments();
        } else {
            document.getElementById('error-message').textContent = response.error;
            document.getElementById('message').textContent = '';
        }
    };

    // Cancella appuntamento
    window.deleteAppointment = async (id) => {
        const res = await fetch(`/appointments/${id}`, {
            method: 'DELETE',
            headers
        });

        const response = await res.json();

        if (res.ok) {
            document.getElementById('message').textContent = response.message;
            document.getElementById('error-message').textContent = '';
            loadAppointments();
        } else {
            document.getElementById('error-message').textContent = response.error;
            document.getElementById('message').textContent = '';
        }
    };

    loadAppointments();
});
