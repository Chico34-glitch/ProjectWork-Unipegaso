document.addEventListener("DOMContentLoaded", function () {
    const tabellaPrenotazioni = document.querySelector("#tabella-prenotazioni-dipendente tbody");

    const token = localStorage.getItem("token");

    async function caricaPrenotazioniDipendente() {
        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazioni_dipendenti", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            const prenotazioni = await response.json();
            tabellaPrenotazioni.innerHTML = "";

            prenotazioni.forEach(p => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${p.email}</td>
                    <td>${p.servizio}</td>
                    <td>${p.data}</td>
                    <td>${p.ora}</td>
                    <td>${p.note || ""}</td>
                `;
                tabellaPrenotazioni.appendChild(row);
            });
        } catch (error) {
            console.error(error);
            alert("Errore nel caricamento delle prenotazioni dipendenti.");
        }
    }

    caricaPrenotazioniDipendente();
});
