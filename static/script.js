function predict() {
    let fileInput = document.getElementById("imageInput");
    let loading = document.getElementById("loading");
    let resultBox = document.getElementById("result");
    let preview = document.getElementById("preview");

    if (fileInput.files.length === 0) {
        alert("Please select an image");
        return;
    }

    let file = fileInput.files[0];
    preview.src = URL.createObjectURL(file);
    preview.classList.remove("hidden");

    let formData = new FormData();
    formData.append("image", file);

    loading.classList.remove("hidden");
    resultBox.classList.add("hidden");

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        loading.classList.add("hidden");
        resultBox.classList.remove("hidden");
        resultBox.innerHTML = `
            <h3>Disease: ${data.disease}</h3>
            <p>Confidence: ${data.confidence}%</p>
        `;
    })
    .catch(err => {
        loading.classList.add("hidden");
        alert("Error: " + err);
    });
}
