document.addEventListener("DOMContentLoaded", async () => {
    await caricaPrenotazioni();
});

async function caricaPrenotazioni() {
    const lista = document.getElementById("lista-prenotazioni");
    lista.innerHTML = "";

    const token = localStorage.getItem("token");

    try {
        const response = await fetch("/prenotazioni", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const prenotazioni = await response.json();

        prenotazioni.forEach(prenotazione => {
            const li = document.createElement("li");
            li.className = "prenotazione";  // questa classe attiva il riquadro bianco

            li.innerHTML = `
                <p><strong>Servizio:</strong> ${prenotazione.servizio}</p>
                <p><strong>Data:</strong> ${prenotazione.data}</p>
                <p><strong>Ora:</strong> ${prenotazione.ora}</p>
                <p><strong>Note:</strong> ${prenotazione.note || "Nessuna nota"}</p>
                <p><strong>Cliente:</strong> ${prenotazione.cliente_email}</p>
                <div class="buttons">
                    <button class="modifica-btn" data-id="${prenotazione.id}">Modifica</button>
                    <button class="cancella-btn" data-id="${prenotazione.id}">Cancella</button>
                </div>
            `;

            // Pulsante Modifica
            li.querySelector(".modifica-btn").addEventListener("click", async () => {
                const nuovoServizio = prompt("Inserisci nuovo servizio:");
                const nuovaData = prompt("Inserisci nuova data (YYYY-MM-DD):");
                const nuovaOra = prompt("Inserisci nuova ora (HH:MM):");
                const nuoveNote = prompt("Inserisci nuove note (puoi lasciare vuoto):");

                if (nuovoServizio && nuovaData && nuovaOra) {
                    try {
                        const response = await fetch(`/modifica_prenotazione/${prenotazione.id}`, {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": "Bearer " + token
                            },
                            body: JSON.stringify({
                                servizio: nuovoServizio,
                                data: nuovaData,
                                ora: nuovaOra,
                                note: nuoveNote
                            })
                        });

                        if (response.ok) {
                            alert("Prenotazione modificata con successo!");
                            caricaPrenotazioni();
                        } else {
                            alert("Errore durante la modifica.");
                        }
                    } catch (error) {
                        console.error("Errore:", error);
                        alert("Errore di connessione al server.");
                    }
                }
            });

            // Pulsante Cancella
            li.querySelector(".cancella-btn").addEventListener("click", async () => {
                const conferma = confirm("Sei sicuro di voler cancellare questa prenotazione?");
                if (conferma) {
                    try {
                        const response = await fetch(`/cancella_prenotazione/${prenotazione.id}`, {
                            method: "DELETE",
                            headers: {
                                "Authorization": "Bearer " + token
                            }
                        });

                        if (response.ok) {
                            alert("Prenotazione cancellata!");
                            caricaPrenotazioni();
                        } else {
                            alert("Errore durante la cancellazione.");
                        }
                    } catch (error) {
                        console.error("Errore:", error);
                        alert("Errore di connessione al server.");
                    }
                }
            });

            lista.appendChild(li);
        });

    } catch (error) {
        console.error("Errore caricando prenotazioni:", error);
        alert("Errore nel caricamento delle prenotazioni.");
    }
}
