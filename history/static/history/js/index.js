document.addEventListener('DOMContentLoaded', function () {
    const option = document.getElementById("sorting")
    const searchField = document.getElementById("searchField")
    const eventModal = document.getElementById('eventModal');
    const closeModalBtn = document.getElementById("cancelEventBtn");
    const overlay = document.getElementById('overlay');


    const urlParams = new URLSearchParams(window.location.search)
    const sortValue = urlParams.get("sort")
    const searchValue = urlParams.get("search")

    if (sortValue) {
        option.value = sortValue;
    }

    if (searchValue) {
        searchField.value = searchValue
    }

    function openModal() {

        // Get user's current scroll position
        const scrollY = window.scrollY;
        const viewportHeight = window.innerHeight;
        const modalHeight = eventModal.clientHeight;

        // Position modal in the center of the current viewport
        eventModal.style.top = `${scrollY + (viewportHeight / 2) - (modalHeight / 2)}px`;
        eventModal.style.left = "50%";
        eventModal.style.transform = "translateX(-50%)";

        eventModal.classList.remove('hidden');
        document.body.style.pointerEvents = "none";
        eventModal.style.pointerEvents = "auto";
        overlay.classList.remove('hidden');

    }

    function closeModal() {
        eventModal.classList.add("hidden");
        document.body.style.pointerEvents = "auto";
        overlay.classList.add('hidden');

    }

    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.addEventListener('click', openModal);
    });

    closeModalBtn.addEventListener("click", closeModal);

    const populateInput = (buttonId, inputId) => {
        const buttons = document.querySelectorAll(`#${buttonId}`);
        buttons.forEach(button => {
            button.addEventListener("click", () => {
                const cell = button.closest('.cell');  // Find the .cell element containing this button
                const ocrText = cell.getAttribute('data-text');  // Get the OCR text from the data-text attribute
                document.querySelector(`#${inputId}`).value = ocrText;  // Populate the corresponding input field
            });
        });
    };

    // Call the function for each button/input pairing
    populateInput("name", "name-input");
    populateInput("start-time", "start-time-input");
    populateInput("start-date", "start-date-input");
    populateInput("location", "location-input");
    populateInput("end-time", "end-time-input");
    populateInput("end-date", "end-date-input");


})