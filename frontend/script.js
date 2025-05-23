document.getElementById("register-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();
        document.getElementById("message").textContent = data.message || data.detail || "Réponse reçue";
    } catch (err) {
        document.getElementById("message").textContent = "Erreur lors de l'envoi du formulaire";
    }
});
