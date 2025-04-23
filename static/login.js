document.addEventListener("DOMContentLoaded", function () {
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");

    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value.trim();

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('ruolo', data.ruolo);

                if (data.ruolo === "cliente") {
                    window.location.href = "/dashboard_cliente";
                } else {
                    window.location.href = "/dashboard_dipendente";
                }
            } else {
                alert(data.error || "Errore durante il login.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });

    formRegister.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("register-email").value.trim();
        const password = document.getElementById("register-password").value.trim();

        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Registrazione completata! Ora puoi effettuare il login.");
            } else {
                alert(data.error || "Errore durante la registrazione.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });
});
