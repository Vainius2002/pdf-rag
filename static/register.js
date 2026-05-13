
const form = document.getElementById("registerForm");
const status = document.getElementById("alert");

document.getElementById("registerForm").addEventListener("submit", async (e) => {   //we use async event, so we can ue await
    e.preventDefault();   //stop the default page reload
    const formData = new FormData(form);   //reads all the form's inputs and packages them up. into formData var.
    const res = await fetch("/register", {method: "POST", body: formData});//we use await to not freeze the page while we POST to /ask

    const data = await res.json();
    if (res.ok) {
        status.textContent = `Created user ${data.username} (id ${data.id})`;
    } else {
        status.textContent = `Error: ${data.detail}`;
    }
});