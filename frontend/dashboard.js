const studentName = document.getElementById("studentName");
const logoutButton = document.getElementById("logoutButton");


async function loadUser() {
    try {
        const response = await fetch("/api/me", {
            method: "GET",
            credentials: "include"
        });

        const data = await response.json();

        if (!response.ok) {
            window.location.href = "/login";
            return;
        }

        studentName.textContent = data.user.name;

    } catch (error) {
        console.error("Could not load user:", error);
        window.location.href = "/login";
    }
}


logoutButton.addEventListener("click", async function () {
    try {
        const response = await fetch("/api/logout", {
            method: "POST",
            credentials: "include"
        });

        if (response.ok) {
            window.location.href = "/login";
        }

    } catch (error) {
        console.error("Logout failed:", error);
    }
});


loadUser();