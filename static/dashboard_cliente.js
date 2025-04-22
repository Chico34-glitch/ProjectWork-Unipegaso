document.addEventListener("DOMContentLoaded", function () {
    const prenotazioneForm = document.getElementById("prenotazione-form");

    prenotazioneForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const token = localStorage.getItem("token");
        const servizio = document.getElementById("servizio").value.trim();
        const data = document.getElementById("data").value.trim();
        const ora = document.getElementById("ora").value.trim();
        const note = document.getElementById("note").value.trim();

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazione", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`  // 🔥 SUPER IMPORTANTE
                },
                body: JSON.stringify({
                    servizio: servizio,
                    data: data,
                    ora: ora,
                    note: note
                })
            });

            const dataResponse = await response.json();

            if (response.ok) {
                alert(dataResponse.message || "Prenotazione avvenuta con successo!");
            } else {
                alert(dataResponse.error || "Errore durante la prenotazione.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });
});
