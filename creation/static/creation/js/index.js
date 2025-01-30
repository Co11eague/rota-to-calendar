document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    const eventModal = document.getElementById('eventModal');
    const openModalBtn = document.getElementById("addEventBtn"); // Update with your button ID
    const closeModalBtn = document.getElementById("cancelEventBtn");


    // Initialize FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/creation/events/', // URL to fetch events
        editable: true,             // Allow event drag-and-drop (optional)
        selectable: true,           // Allow date selection (optional)

        eventClick: function (info) {
            // Gather the necessary data to be sent to the convert view
            var eventTitle = info.event.title;
            var eventStart = info.event.start;
            var eventEnd = info.event.end;
            var eventLocation = info.event.extendedProps.location;

            console.log(eventEnd)

            var eventStartDate = eventStart.toISOString().split('T')[0];  // Extract the date part
            var eventEndDate = eventEnd.toISOString().split('T')[0];      // Extract the date part
            var eventStartTime = eventStart.toTimeString().split(' ')[0].substring(0, 5);  // HH:MM format
            var eventEndTime = eventEnd.toTimeString().split(' ')[0].substring(0, 5);    // HH:MM format

            // Prepare the POST data
            var data = new FormData();
            data.append("Name", eventTitle);
            data.append("Location", eventLocation);
            data.append("Start Date", eventStartDate);
            data.append("End Date", eventEndDate);
            data.append("Start Time", eventStartTime);
            data.append("End Time", eventEndTime);
            data.append("action", "convert");

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
            var title = prompt("Enter event title:");
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: info.startStr,
                    end: info.endStr,
                    allDay: info.allDay
                });
                // Now save the event in the database (server-side)
                fetch('/creation/add_event/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded', // Correct content type
                    },
                    body: `title=${title}&start=${info.startStr}&end=${info.endStr}`,
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Event added successfully!');
                        } else {
                            console.log('Failed to add event.');
                        }
                    });
            }


            calendar.unselect(); // Unselect the date after creating the event
        }

    });

    function openModal() {
        eventModal.classList.remove('hidden');
        document.body.style.pointerEvents = "none";
        eventModal.style.pointerEvents = "auto";
    }

    function closeModal() {
        eventModal.classList.add("hidden");
        document.body.style.pointerEvents = "auto";

    }

    openModalBtn.addEventListener("click", openModal);
    closeModalBtn.addEventListener("click", closeModal);


    document.getElementById('addEventBtn').addEventListener('click', function () {

        eventModal.classList.remove('hidden');
        document.body.style.pointerEvents = "none";

        // var title = prompt("Enter event title:");
        // var startDate = prompt("Enter event start date and time (YYYY-MM-DDTHH:MM):");
        // var endDate = prompt("Enter event end date and time (YYYY-MM-DDTHH:MM):");
        //
        // if (title && startDate && endDate) {
        //     // Add the event to the calendar
        //     calendar.addEvent({
        //         title: title,
        //         start: startDate,
        //         end: endDate
        //     });
        //
        //     fetch('/creation/add_event/', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/x-www-form-urlencoded', // Correct content type
        //         },
        //         body: `title=${title}&start=${startDate}&end=${endDate}`,
        //     })
        //         .then(response => response.json())
        //         .then(data => {
        //             if (data.success) {
        //                 console.log('Event added successfully!');
        //             } else {
        //                 console.log('Failed to add event.');
        //             }
        //         });
        // }
    });
    calendar.render(); // Render the calendar
});