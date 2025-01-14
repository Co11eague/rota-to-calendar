import urllib.parse
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ics import Calendar, Event

from conversion.models import UploadedTable, TableCell


@login_required
def index(request):
	tables = UploadedTable.objects.all()
	return render(request, 'history/index.html', {'tables': tables})


@login_required
# Create your views here.
def view_cells(request, table_id):
	# Fetch the selected table
	table = get_object_or_404(UploadedTable, id=table_id)
	# Fetch all cells related to this table
	cells = TableCell.objects.filter(table=table)
	return render(request, 'history/view_cells.html', {'table': table, 'cells': cells})


@csrf_exempt
def convert(request):
	if request.method == 'POST':
		# Gather the form data
		name = str(request.POST.get('Name'))
		location = str(request.POST.get('Location'))
		start_date = str(request.POST.get('Start Date'))
		end_date = str(request.POST.get('End Date'))
		start_time = str(request.POST.get('Start Time'))
		end_time = str(request.POST.get('End Time'))
		action = request.POST.get('action')  # Check which button was clicked

		try:
			start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
			end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
		except ValueError:
			return HttpResponse(
				"Invalid date/time format. Please use YYYY-MM-DD for dates and HH:MM (24-hour format) for times.",
				status=400)

		if action == 'convert':

			# Convert start and end datetime

			# Create calendar event
			c = Calendar()
			e = Event()
			e.name = name
			e.begin = start_datetime
			e.end = end_datetime
			e.location = location
			e.description = "Test"
			c.events.add(e)

			# Generate the .ics file
			ics_content = c.serialize()

			# Create response to download the file
			response = HttpResponse(ics_content, content_type='text/calendar')
			response['Content-Disposition'] = f'attachment; filename="{name.replace(" ", "_")}_event.ics"'
			return response
		else:
			google_calendar_url = (
					"https://calendar.google.com/calendar/render?"
					+ urllib.parse.urlencode({
				"action": "TEMPLATE",
				"text": name,  # Event title
				"details": f"Event at {location}",  # Event details
				"location": location,
				"dates": f"{start_datetime.strftime('%Y%m%dT%H%M%S')}/{end_datetime.strftime('%Y%m%dT%H%M%S')}",
				"sf": "true",
				"output": "xml"  # Optional: opens in Google's event editor
			})
			)

			# Redirect to Google Calendar
			return redirect(google_calendar_url)

	return HttpResponse("Invalid request method", status=405)
