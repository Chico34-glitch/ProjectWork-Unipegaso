document.addEventListener("DOMContentLoaded", function () {
    const formPrenotazione = document.getElementById("form-prenotazione");

    formPrenotazione.addEventListener("submit", async (e) => {
        e.preventDefault();

        const servizio = document.getElementById("servizio").value;
        const data = document.getElementById("data").value;
        const ora = document.getElementById("ora").value;
        const note = document.getElementById("note").value;

        const token = localStorage.getItem("token");

        try {
            const response = await fetch("/prenotazioni", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({ servizio, data, ora, note })
            });

            if (response.ok) {
                alert("Prenotazione effettuata con successo!");
                formPrenotazione.reset();
                caricaPrenotazioni();
            } else {
                const data = await response.json();
                alert(data.error || "Errore durante la prenotazione.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });

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
                const li = document.createElement("li");
                li.className = "prenotazione";

                li.innerHTML = `
                    <p><strong>Servizio:</strong> ${prenotazione.servizio}</p>
                    <p><strong>Data:</strong> ${prenotazione.data}</p>
                    <p><strong>Ora:</strong> ${prenotazione.ora}</p>
                    <p><strong>Note:</strong> ${prenotazione.note || "Nessuna nota"}</p>
                    <div class="buttons">
                        <button class="modifica-btn">Modifica</button>
                        <button class="cancella-btn">Cancella</button>
                    </div>
                `;

                // Bottone MODIFICA
                li.querySelector(".modifica-btn").addEventListener("click", async () => {
                    const nuovoServizio = prompt("Nuovo Servizio:", prenotazione.servizio);
                    const nuovaData = prompt("Nuova Data (YYYY-MM-DD):", prenotazione.data);
                    const nuovaOra = prompt("Nuova Ora (HH:MM):", prenotazione.ora);
                    const nuoveNote = prompt("Nuove Note:", prenotazione.note);

                    if (nuovoServizio && nuovaData && nuovaOra) {
                        try {
                            const response = await fetch(`/modifica_prenotazione_cliente/${prenotazione.id}`, {
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
                                alert("Prenotazione modificata!");
                                caricaPrenotazioni();
                            } else {
                                alert("Errore nella modifica.");
                            }
                        } catch (error) {
                            console.error("Errore:", error);
                            alert("Errore di connessione al server.");
                        }
                    }
                });

                // Bottone CANCELLA
                li.querySelector(".cancella-btn").addEventListener("click", async () => {
                    const conferma = confirm("Vuoi cancellare questa prenotazione?");
                    if (conferma) {
                        try {
                            const response = await fetch(`/cancella_prenotazione_cliente/${prenotazione.id}`, {
                                method: "DELETE",
                                headers: {
                                    "Authorization": "Bearer " + token
                                }
                            });

                            if (response.ok) {
                                alert("Prenotazione cancellata.");
                                caricaPrenotazioni();
                            } else {
                                alert("Errore nella cancellazione.");
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

    caricaPrenotazioni();
});
