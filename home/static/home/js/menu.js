document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('features-btn');
    const dropdown = document.getElementById('features-dropdown');

    button.addEventListener('click', function () {
        dropdown.classList.toggle('hidden'); // Toggles visibility of the dropdown
    });
});