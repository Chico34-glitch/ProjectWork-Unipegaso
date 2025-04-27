document.addEventListener("DOMContentLoaded", () => {
    caricaPrenotazioni();

    const formPrenotazione = document.getElementById("form-prenotazione");
    formPrenotazione.addEventListener("submit", async (e) => {
        e.preventDefault();
        await creaPrenotazione();
    });
});

async function creaPrenotazione() {
    const servizio = document.getElementById("servizio").value.trim();
    const dataServizio = document.getElementById("data").value.trim();
    const ora = document.getElementById("ora").value.trim();
    const note = document.getElementById("note").value.trim();
    const token = localStorage.getItem("token");

    if (!servizio || !dataServizio || !ora) {
        alert("Compila tutti i campi obbligatori!");
        return;
    }

    try {
        const response = await fetch("/prenotazione", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ servizio, data: dataServizio, ora, note })
        });

        if (response.ok) {
            alert("Prenotazione effettuata con successo!");
            document.getElementById("form-prenotazione").reset();
            caricaPrenotazioni();
        } else {
            const err = await response.json();
            alert(err.error || "Errore durante la prenotazione.");
        }
    } catch (error) {
        console.error("Errore prenotazione:", error);
    }
}

async function caricaPrenotazioni() {
    const lista = document.getElementById("lista-prenotazioni");
    lista.innerHTML = "";

    const token = localStorage.getItem("token");

    try {
        const response = await fetch("/prenotazioni_cliente", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const prenotazioni = await response.json();

        prenotazioni.forEach(prenotazione => {
            const div = document.createElement("div");
            div.className = "prenotazione";
            div.innerHTML = `
                <p><strong>Servizio:</strong> ${prenotazione.servizio}</p>
                <p><strong>Data:</strong> ${prenotazione.data}</p>
                <p><strong>Ora:</strong> ${prenotazione.ora}</p>
                <p><strong>Note:</strong> ${prenotazione.note || "Nessuna nota"}</p>
                <button class="modifica" data-id="${prenotazione.id}">Modifica</button>
                <button class="cancella" data-id="${prenotazione.id}">Cancella</button>
            `;
            lista.appendChild(div);
        });

        document.querySelectorAll(".modifica").forEach(button => {
            button.addEventListener("click", () => {
                const id = button.dataset.id;
                modificaPrenotazione(id);
            });
        });

        document.querySelectorAll(".cancella").forEach(button => {
            button.addEventListener("click", () => {
                const id = button.dataset.id;
                cancellaPrenotazione(id);
            });
        });

    } catch (error) {
        console.error("Errore caricando prenotazioni:", error);
        alert("Errore nel caricamento delle prenotazioni.");
    }
}

async function modificaPrenotazione(id) {
    const nuovoServizio = prompt("Inserisci nuovo servizio:");
    const nuovaData = prompt("Inserisci nuova data (YYYY-MM-DD):");
    const nuovaOra = prompt("Inserisci nuova ora (HH:MM):");
    const nuoveNote = prompt("Inserisci nuove note (puoi lasciare vuoto):");

    if (nuovoServizio && nuovaData && nuovaOra) {
        const token = localStorage.getItem("token");

        try {
            const response = await fetch(`/modifica_prenotazione_cliente/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({ servizio: nuovoServizio, data: nuovaData, ora: nuovaOra, note: nuoveNote })
            });

            if (response.ok) {
                alert("Prenotazione modificata!");
                caricaPrenotazioni();
            } else {
                alert("Errore nella modifica della prenotazione.");
            }
        } catch (error) {
            console.error("Errore modifica:", error);
        }
    }
}

async function cancellaPrenotazione(id) {
    if (confirm("Sei sicuro di voler cancellare questa prenotazione?")) {
        const token = localStorage.getItem("token");

        try {
            const response = await fetch(`/cancella_prenotazione_cliente/${id}`, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            if (response.ok) {
                alert("Prenotazione cancellata!");
                caricaPrenotazioni();
            } else {
                alert("Errore nella cancellazione della prenotazione.");
            }
        } catch (error) {
            console.error("Errore cancellazione:", error);
        }
    }
}
