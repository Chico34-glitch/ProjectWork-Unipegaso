document.addEventListener("DOMContentLoaded", function () {
    const prenotazioneForm = document.getElementById("prenotazione-form");
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Token non trovato! Effettua il login.");
        window.location.href = "/";
        return;
    }

    prenotazioneForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const servizio = document.getElementById("servizio").value;
        const data = document.getElementById("data").value;
        const ora = document.getElementById("ora").value;
        const note = document.getElementById("note").value;

        // Validazione base
        if (!servizio || !data || !ora) {
            alert("Inserisci tutti i campi obbligatori.");
            return;
        }

        const payload = {
            servizio: servizio,
            data: data,
            ora: ora,
            note: note || ""
        };

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazione", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message || "Prenotazione avvenuta con successo!");
                prenotazioneForm.reset();
            } else {
                alert(result.error || "Errore nella prenotazione.");
            }
        } catch (error) {
            console.error("Errore:", error);
            alert("Errore di connessione al server.");
        }
    });
});
