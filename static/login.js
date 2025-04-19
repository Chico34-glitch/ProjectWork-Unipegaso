document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // Salva il token JWT nel localStorage
                localStorage.setItem("token", data.access_token);

                // Reindirizza alla dashboard corretta
                if (data.ruolo === "cliente") {
                    window.location.href = "/dashboard_cliente";
                } else if (data.ruolo === "dipendente") {
                    window.location.href = "/dashboard_dipendente";
                }
            } else {
                alert(data.error || "Errore durante il login. Riprova.");
            }
        } catch (error) {
            console.error("Errore di connessione:", error);
            alert("Errore di connessione al server. Controlla che il server sia attivo.");
        }
    });
});
