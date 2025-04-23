document.addEventListener("DOMContentLoaded", function () {
    const prenotazioneForm = document.getElementById("prenotazione-form");

    const token = localStorage.getItem('token');

    prenotazioneForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const servizio = document.getElementById("servizio").value;
        const data = document.getElementById("data").value;
        const ora = document.getElementById("ora").value;
        const note = document.getElementById("note").value;

        try {
            const response = await fetch("http://127.0.0.1:5000/prenotazione", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
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
                alert(dataResponse.error || "Errore nella prenotazione.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });
});
