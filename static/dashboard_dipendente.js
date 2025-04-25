document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");

    async function caricaPrenotazioni() {
        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazioni", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });
            const prenotazioni = await response.json();

            const lista = document.getElementById("lista-prenotazioni");
            lista.innerHTML = "";

            prenotazioni.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <strong>Email cliente:</strong> ${p.cliente_email} |
                    <strong>Servizio:</strong> ${p.servizio} |
                    <strong>Data:</strong> ${p.data} |
                    <strong>Ora:</strong> ${p.ora} |
                    <strong>Note:</strong> ${p.note}
                    <button onclick="modificaPrenotazione(${p.id})">Modifica</button>
                    <button onclick="cancellaPrenotazione(${p.id})">Cancella</button>
                `;
                lista.appendChild(li);
            });

        } catch (error) {
            console.error("Errore nel caricamento delle prenotazioni:", error);
        }
    }

    window.modificaPrenotazione = async function (id) {
        const nuovoServizio = prompt("Nuovo servizio:");
        const nuovaData = prompt("Nuova data (YYYY-MM-DD):");
        const nuovaOra = prompt("Nuova ora (HH:MM):");
        const nuoveNote = prompt("Note aggiornate:");

        if (nuovoServizio && nuovaData && nuovaOra) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/modifica_prenotazione/${id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        servizio: nuovoServizio,
                        data: nuovaData,
                        ora: nuovaOra,
                        note: nuoveNote
                    })
                });

                if (response.ok) {
                    alert("Prenotazione modificata!");
                    caricaPrenotazioni();
                } else {
                    alert("Errore nella modifica.");
                }
            } catch (error) {
                console.error("Errore:", error);
            }
        }
    };

    window.cancellaPrenotazione = async function (id) {
        if (confirm("Vuoi davvero cancellare questa prenotazione?")) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/cancella_prenotazione/${id}`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    alert("Prenotazione cancellata!");
                    caricaPrenotazioni();
                } else {
                    alert("Errore nella cancellazione.");
                }
            } catch (error) {
                console.error("Errore:", error);
            }
        }
    };

    caricaPrenotazioni();
});
