document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    const eventModal = document.getElementById('eventModal');
    const openModalBtn = document.getElementById("addEventBtn"); // Update with your button ID
    const closeModalBtn = document.getElementById("cancelEventBtn");
    const overlay = document.getElementById('overlay');
    const form = document.getElementById('add-shift');

    var startField = form.querySelector("[name='start']");
    var endField = form.querySelector("[name='end']");


    // Initialize FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/creation/events/', // URL to fetch events
        editable: true,             // Allow event drag-and-drop (optional)
        selectable: true,           // Allow date selection (optional)

        eventClick: function (info) {

            var eventTitle = info.event.title;
            var eventStart = info.event.start;
            var eventEnd = info.event.end;
            var eventDescription = info.event.extendedProps.description;

            console.log(eventEnd)

            var eventStartDate = eventStart.toISOString().split('T')[0];
            var eventEndDate = eventEnd.toISOString().split('T')[0];
            var eventStartTime = eventStart.toTimeString().split(' ')[0].substring(0, 5);
            var eventEndTime = eventEnd.toTimeString().split(' ')[0].substring(0, 5);

            // Prepare the POST data
            var data = new FormData();
            data.append("title", eventTitle);
            data.append("location", eventDescription)
            data.append("start_date", eventStartDate);
            data.append("end_date", eventEndDate);
            data.append("start_time", eventStartTime);
            data.append("end_time", eventEndTime);
            data.append("action", "convert+");


            fetch("/history/calendar-convert/", {
                method: "POST",
                body: data
            }).then(response => response.blob())
                .then(blob => {
                    var downloadUrl = window.URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = `${eventTitle.replace(" ", "_")}_event.ics`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }).catch(error => console.error("Error:", error));
        },

        select: function (info) {
            openModal()

            var eventStart = info.startStr;
            var eventEnd = info.endStr;

            // Combine date and time to get the 'YYYY-MM-DDTHH:MM' format
            var startDateTime = eventStart + "T" + "12:00";
            var endDateTime = eventEnd + "T" + "12:00";

            startField.value = startDateTime
            endField.value = endDateTime

            calendar.unselect(); // Unselect the date after creating the event
        }

    });

    function openModal() {
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

    openModalBtn.addEventListener("click", openModal);
    closeModalBtn.addEventListener("click", closeModal);

    calendar.render(); // Render the calendar
});