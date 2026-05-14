const token = localStorage.getItem("token");
if (!token) {
    document.getElementById("answer").textContent = "Not logged in. Go to /login first.";
    window.location.href = "/login";
}

document.getElementById("askForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const pdfFile = form.querySelector('input[name="pdf"]').files[0];
    const question = form.querySelector('input[name="question"]').value;

    // Step 1: upload the PDF
    const uploadData = new FormData();
    uploadData.append("pdf", pdfFile);

    const uploadRes = await fetch("/upload", {
        method: "POST",
        headers: {"authorization" : `Bearer ${token}` },
        body: uploadData,
    });

    if (!uploadRes.ok) {
        const err = await uploadRes.json();
        document.getElementById("answer").textContent = `Upload error: ${err.detail}`;
        return;
    }

    const { document_id } = await uploadRes.json();

    // Step 2: ask the question against that document
    const askData = new FormData();
    askData.append("document_id", document_id);
    askData.append("question", question);

    const askRes = await fetch("/ask", {
        method: "POST",
        headers: {"authorization" : `Bearer ${token}` },
        body: askData,
    });

    const data = await askRes.json();
    document.getElementById("answer").textContent = askRes.ok ? data.answer : `Ask error: ${data.detail}`;
});
