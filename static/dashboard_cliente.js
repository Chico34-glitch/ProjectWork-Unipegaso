document.addEventListener("DOMContentLoaded", function () {
    const prenotazioneForm = document.getElementById("prenotazione-form");
    const tabellaPrenotazioni = document.querySelector("#tabella-prenotazioni tbody");

    const token = localStorage.getItem("token");

    async function caricaPrenotazioni() {
        if (!token) {
            console.error("Token non trovato. Devi loggarti prima.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazioni_cliente", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Errore durante il caricamento:", errorData.msg);
                alert(errorData.msg || "Errore durante il caricamento delle prenotazioni.");
                return;
            }

            const prenotazioni = await response.json();
            tabellaPrenotazioni.innerHTML = "";

            prenotazioni.forEach(p => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${p.servizio}</td>
                    <td>${p.data}</td>
                    <td>${p.ora}</td>
                    <td>${p.note || ""}</td>
                `;
                tabellaPrenotazioni.appendChild(row);
            });
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    }

    prenotazioneForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const servizio = document.getElementById("servizio").value.trim();
        const data = document.getElementById("data").value;
        const ora = document.getElementById("ora").value;
        const note = document.getElementById("note").value.trim();

        if (!servizio || !data || !ora) {
            alert("Tutti i campi tranne le note sono obbligatori!");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazione", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ servizio, data, ora, note })
            });

            if (response.ok) {
                const dataResponse = await response.json();
                alert(dataResponse.message || "Prenotazione avvenuta con successo!");
                caricaPrenotazioni();
            } else {
                const errorData = await response.json();
                alert(errorData.error || "Errore durante la prenotazione.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });

    caricaPrenotazioni();
});
