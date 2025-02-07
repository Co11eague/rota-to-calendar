document.addEventListener('DOMContentLoaded', function () {

    const closeModalBtn = document.getElementById("cancelEventBtn");

    const overlay = document.getElementById('overlay');

    const eventModal = document.getElementById('eventModal');
    const modalText = document.getElementById("modal-text");
    const modalImage = document.getElementById("modal-image");


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

    function parseFlexibleDate(input) {
        return Sugar.Date.create(input, {fromUTC: false});
    }

    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.addEventListener('click', openModal);
    });

    closeModalBtn.addEventListener("click", closeModal);

    const populateTextInput = (buttonId, inputId) => {
        const button = document.getElementById(buttonId);

        if (button) {
            button.addEventListener("click", function () {
                const dataText = modalText.value;

                const inputField = document.querySelector(`#${inputId}`);
                if (inputField) {
                    inputField.value = dataText;  // Populate the corresponding input field
                    displayToast("Data was successfully inserted.", "success")
                } else {
                    displayToast("There was an issue inserting your data.", "error")
                }

                closeModal()
            });
        }
    };


    const populateTimeInput = (buttonId, inputId) => {
        const button = document.getElementById(buttonId);


        if (button) {
            button.addEventListener("click", function () {
                const dataText = modalText.value;

                const time = moment(dataText, [
                    "h A", "h:mm A", "h:mm:ss A", "h:mm:ss.SSS A",
                    "hh A", "hh:mm A", "hh:mm:ss A", "hh:mm:ss.SSS A",
                    "H", "HH", "H:mm", "HH:mm", "H:mm:ss", "HH:mm:ss",
                    "H:mm:ss.SSS", "HH:mm:ss.SSSS"
                ], true)

                if (time.isValid()) {


                    const inputField = document.querySelector(`#${inputId}`);
                    if (inputField) {
                        inputField.value = time.format("HH:mm");  // Populate the corresponding input field
                        displayToast("Your time was successfully inserted.")
                    } else {
                        displayToast("There was an issue inserting your time.", "error")
                    }

                    closeModal()
                } else {
                    displayToast("There was an issue understanding time format.", "error")
                }
            });
        }
    };

    const populateDateInput = (buttonId, inputId) => {
        const button = document.getElementById(buttonId);

        if (button) {
            button.addEventListener("click", function () {
                const dataText = modalText.value;
                const parsed_date = parseFlexibleDate(dataText)

                if (isNaN(parsed_date)) displayToast("There was an issue understanding the date format.", "error");
                else {
                    const inputField = document.querySelector(`#${inputId}`);
                    if (inputField) {
                        inputField.value = Sugar.Date.format(parsed_date, '{yyyy}-{MM}-{dd}');  // Populate the corresponding input field
                        displayToast("Your date was successfully inserted.", "success")
                    } else {
                        displayToast("There was an issue inserting your date.", "error")
                    }
                    closeModal()
                }
            });
        }
    };

    function displayToast(message, tags) {
        const isDarkMode = document.documentElement.classList.contains("dark");

        // Define background colors based on tags
        const bgColor = isDarkMode
            ? (tags === 'success' ? "#16a34a" : tags === 'error' ? "#b91c1c" : "#1e40af")
            : (tags === 'success' ? "#22c55e" : tags === 'error' ? "#ef4444" : "#3b82f6");

        // Show toast notification
        Toastify({
            text: message,
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: bgColor,
            close: true
        }).showToast();
    }


    // Call the function for each button/input pairing
    populateTextInput("title", "title-input");
    populateTextInput("location", "location-input");
    populateTimeInput("start-time", "start-time-input");
    populateDateInput("start-date", "start-date-input");
    populateTimeInput("end-time", "end-time-input");
    populateDateInput("end-date", "end-date-input");

})