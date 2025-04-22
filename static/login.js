document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("ruolo", data.ruolo);

                if (data.ruolo === "cliente") {
                    window.location.href = "/dashboard_cliente";
                } else if (data.ruolo === "dipendente") {
                    window.location.href = "/dashboard_dipendente";
                }
            } else {
                alert(data.error || "Errore di login.");
            }
        } catch (error) {
            console.error(error);
            alert("Errore di connessione al server.");
        }
    });
});
