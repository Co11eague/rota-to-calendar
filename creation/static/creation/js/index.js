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
            var eventDescription = info.event.description;

            console.log(eventEnd)

            var eventStartDate = eventStart.toISOString().split('T')[0];
            var eventEndDate = eventEnd.toISOString().split('T')[0];
            var eventStartTime = eventStart.toTimeString().split(' ')[0].substring(0, 5);
            var eventEndTime = eventEnd.toTimeString().split(' ')[0].substring(0, 5);

            // Prepare the POST data
            var data = new FormData();
            data.append("Name", eventTitle);
            data.append("Location", null);
            data.append("Description", eventDescription)
            data.append("Start Date", eventStartDate);
            data.append("End Date", eventEndDate);
            data.append("Start Time", eventStartTime);
            data.append("End Time", eventEndTime);
            data.append("action", "convert+");

            // Make the POST request to trigger ICS file download
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/history/calendar-convert/", true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // If successful, this should initiate download of the .ics file
                    var blob = xhr.response;
                    var downloadUrl = window.URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = `${eventTitle.replace(" ", "_")}_event.ics`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } else {
                    console.error('Failed to generate ICS file.');
                }
            };
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.responseType = 'blob';  // Ensure the response is treated as a file (blob)
            xhr.send(data);
        },

        select: function (info) {
            openModal()

            var eventStart = info.event.start;
            var eventEnd = info.event.end;

            // Convert the event start time to the format 'YYYY-MM-DDTHH:MM'
            var startDate = eventStart.toISOString().split('T')[0];  // 'YYYY-MM-DD'
            var startTime = eventStart.toTimeString().split(' ')[0].substring(0, 5);  // 'HH:MM'

            var endDate = eventEnd.toISOString().split('T')[0];  // 'YYYY-MM-DD'
            var endTime = eventEnd.toTimeString().split(' ')[0].substring(0, 5);  // 'HH:MM'

            // Combine date and time to get the 'YYYY-MM-DDTHH:MM' format
            var startDateTime = startDate + "T" + startTime;
            var endDateTime = endDate + "T" + endTime;

            startField.value = startDateTime
            endField.value = endDateTime

            form.submit()
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