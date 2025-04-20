document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    // Gestione Login
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.access_token);

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

    // Gestione Registrazione
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("reg-email").value;
        const password = document.getElementById("reg-password").value;

        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Registrazione completata! Ora puoi accedere.");
            } else {
                alert(data.error || "Errore durante la registrazione.");
            }
        } catch (error) {
            console.error("Errore di connessione:", error);
            alert("Errore di connessione al server. Controlla che il server sia attivo.");
        }
    });
});
