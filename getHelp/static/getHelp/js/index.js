// Wait for the document to load
document.addEventListener("DOMContentLoaded", function () {
    const helpTypeField = document.querySelector('input[name="helpType"]');
    const fileDiv = document.getElementById("file");

    // Add an event listener for changes to the RadioSelect field
    document.querySelectorAll('input[name="helpType"]').forEach((radio) => {
        radio.addEventListener("change", function () {
            if (this.value === "fine-tuning") {
                fileDiv.classList.remove("hidden");
            } else {
                fileDiv.classList.add("hidden");
            }
        });
    });

    // Initial check to set visibility based on the default value
    const checkedValue = helpTypeField.checked ? helpTypeField.value : null;
    if (checkedValue === "fine-tuning") {
        fileDiv.classList.remove("hidden");
    }
});

function handleDrop(event) {
    event.preventDefault();
    const fileInput = document.getElementById("id_file");
    const files = event.dataTransfer.files;

    if (files.length > 0) {
        fileInput.files = files;
    }
}