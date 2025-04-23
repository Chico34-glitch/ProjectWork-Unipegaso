document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");

    async function caricaPrenotazioni() {
        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazioni", {
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

    caricaPrenotazioni();
});
