 document.addEventListener("DOMContentLoaded", function () {
     const fileInput = document.querySelector('input[name="profile_picture"]'); // This targets the profile_picture input field
     const clearButton = document.getElementById('clear-button');
     const previewImage = document.getElementById('preview-image');
     const previewPlaceholder = document.getElementById('preview-placeholder');

        fileInput.addEventListener('change', function(event) {
            const previewImage = document.getElementById('preview-image');
            const imageContainer = document.getElementById('image-preview-container');
            const file = event.target.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Set the image preview to the uploaded file
                    previewImage.src = e.target.result;
                    previewImage.classList.remove('hidden');
                    imageContainer.querySelector('#preview-placeholder').classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });

     clearButton.addEventListener('click', function () {
         fileInput.value = '';  // Reset the file input
         previewImage.src = '';  // Clear the preview image
         previewImage.classList.add('hidden');  // Hide the preview image
         previewPlaceholder.classList.remove('hidden');  // Show the placeholder text
     });

 })