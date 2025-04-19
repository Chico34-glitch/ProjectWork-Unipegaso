document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const body = { email, password };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.access_token);

            const payload = JSON.parse(atob(data.access_token.split('.')[1]));

            if (payload.identity.ruolo === 'cliente') {
                window.location.href = '/dashboard_cliente';
            } else if (payload.identity.ruolo === 'dipendente') {
                window.location.href = '/dashboard_dipendente';
            }
        } else {
            document.getElementById('error-message').textContent = data.error;
        }
    } catch (error) {
        console.error('Errore di connessione:', error);
        document.getElementById('error-message').textContent = "Errore di connessione.";
    }
});
