document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('input[name="image"]');

    fileInput.addEventListener('change', function (event) {
        const previewImage = document.getElementById('preview-image');
        const file = event.target.files[0];
        console.log("HERE")

        if (file) {
            if (!file.type.startsWith('image/')) {
                alert('Please select a valid image file.');
                fileInput.value = ''; // Clear the input value
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                // Display the uploaded image preview
                previewImage.src = e.target.result;
                previewImage.classList.remove('hidden');
                previewPlaceholder.classList.add('hidden');
            };
            reader.onerror = function () {
                alert('Could not preview this file. Try another.');
            };
            reader.readAsDataURL(file);
        } else {
            // Reset to default when no file is selected
            previewImage.classList.add('hidden');
            previewImage.src = '';
            previewPlaceholder.classList.remove('hidden');
        }
    });
})