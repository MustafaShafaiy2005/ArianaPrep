const registerForm = document.getElementById("registerForm");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            message.textContent = "Account created successfully!";

            setTimeout(function () {
                window.location.href = "/login";
            }, 500);
        } else {
            message.textContent = data.error || "Registration failed.";
        }

    } catch (error) {
        message.textContent = "Could not connect to ArianaPrep backend.";
        console.error(error);
    }
});