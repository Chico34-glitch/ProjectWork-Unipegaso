document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token"); // 🔐 Legge il token JWT salvato al login

    async function caricaPrenotazioni() {
        const lista = document.getElementById("lista-prenotazioni");

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazioni", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json"
                }
            });

            lista.innerHTML = ""; // Pulisce la lista

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
                console.error("Errore HTTP:", response.status);
            }

        } catch (err) {
            console.error("Errore di connessione:", err);
            lista.innerHTML = "<li>Errore di connessione al server.</li>";
        }
    }

    caricaPrenotazioni();
});
