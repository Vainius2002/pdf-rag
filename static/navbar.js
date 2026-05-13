document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    const logout = document.getElementById("logoutLink");
    const login = document.getElementById("loginLink");
    const register = document.getElementById("registerLink");

    // Show "Logout" only when logged in; hide Login/Register when logged in.
    if (token) {
        if (login) login.style.display = "none";
        if (register) register.style.display = "none";
    } else {
        if (logout) logout.style.display = "none";
    }

    if (logout) {
        logout.addEventListener("click", (e) => {
            e.preventDefault();
            localStorage.removeItem("token");
            window.location.href = "/login";
        });
    }
});
