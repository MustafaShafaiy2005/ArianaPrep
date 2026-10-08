const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");


loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;


    try {

        const response = await fetch("/api/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            credentials: "include",

            body: JSON.stringify({
                email: email,
                password: password
            })

        });


        const data = await response.json();


        if (response.ok) {

            message.textContent = "Login successful!";

            setTimeout(function () {
                window.location.href = "/dashboard";
            }, 500);

        } else {

            message.textContent =
                data.error || "Login failed.";

        }


    } catch (error) {

        message.textContent =
            "Could not connect to ArianaPrep backend.";

        console.error(error);

    }

});