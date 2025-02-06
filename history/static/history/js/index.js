document.addEventListener('DOMContentLoaded', function () {
    const option = document.getElementById("sorting")
    const searchField = document.getElementById("searchField")
    const eventModal = document.getElementById('eventModal');
    const closeModalBtn = document.getElementById("cancelEventBtn");
    const overlay = document.getElementById('overlay');
    const modalText = document.getElementById("modal-text");
    const modalImage = document.getElementById("modal-image");

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

        const ocrText = this.getAttribute("data-text");
        const imageUrl = this.getAttribute("data-image");

        // Update modal content
        modalText.value = ocrText;
        modalImage.src = imageUrl;

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
        const button = document.getElementById(buttonId);

        if (button) {
            button.addEventListener("click", function () {
                const dataText = modalText.value;

                const inputField = document.querySelector(`#${inputId}`);
                if (inputField) {
                    inputField.value = dataText;  // Populate the corresponding input field
                } else {
                    console.warn(`No input field found with ID: ${inputId}`);
                }

                closeModal()
            });
        }
    };

    // Call the function for each button/input pairing
    populateInput("title", "title-input");
    populateInput("start-time", "start-time-input");
    populateInput("start-date", "start-date-input");
    populateInput("location", "location-input");
    populateInput("end-time", "end-time-input");
    populateInput("end-date", "end-date-input");


})