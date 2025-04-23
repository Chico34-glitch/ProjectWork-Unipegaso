document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("prenotazione-form");
    const token = localStorage.getItem("token");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const servizio = document.getElementById("servizio").value;
        const data = document.getElementById("data").value;
        const ora = document.getElementById("ora").value;
        const note = document.getElementById("note").value;

        const payload = { servizio, data, ora, note };

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazione", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message || "Prenotazione avvenuta con successo!");
                form.reset();
                caricaPrenotazioni(); // Ricarica prenotazioni
            } else {
                alert(result.error || "Errore nella prenotazione.");
            }
        } catch (err) {
            console.error("Errore di connessione:", err);
            alert("Connessione al server non riuscita.");
        }
    });

    caricaPrenotazioni(); // Carica all'avvio
});

async function caricaPrenotazioni() {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch("http://127.0.0.1:5000/prenotazioni_cliente", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const lista = document.getElementById("lista-prenotazioni");
        lista.innerHTML = "";

        if (response.ok) {
            const dati = await response.json();
            if (dati.length === 0) {
                lista.innerHTML = "<li>Nessuna prenotazione trovata.</li>";
                return;
            }

            dati.forEach(p => {
                const voce = document.createElement("li");
                voce.textContent = `${p.data} alle ${p.ora} - ${p.servizio} (${p.note})`;
                lista.appendChild(voce);
            });
        } else {
            lista.innerHTML = "<li>Errore nel caricamento delle prenotazioni.</li>";
        }
    } catch (err) {
        console.error("Errore nel recupero prenotazioni:", err);
    }
}
