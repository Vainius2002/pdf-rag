const form = document.getElementById("loginForm");
const msg = document.getElementById("message");

form.addEventListener("submit", async(e) =>{
    e.preventDefault();

    formData = new FormData(form);
    const res = await fetch("/login", {method:"POST", body:formData});

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("token", data.access_token); //we store the token we receive into browsers local storage as key 'token'. This way we can use it in future requests
        msg.textContent = "Logged in! Token saved.";
    } else {
        msg.textContent = `Error: ${data.detail}`;
    }
});