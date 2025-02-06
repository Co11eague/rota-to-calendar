import urllib.parse
from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ics import Calendar, Event
from schedule.models import Calendar as LocalCalendar
from schedule.models import Event as LocalEvent  # Assuming you're using django-scheduler's Event model

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings
from conversion.models import UploadedTable, TableCell
from history.forms import CalendarForm


@login_required
def index(request):

	VALID_SORT_FIELDS = ["title", "uploaded_at", "-uploaded_at", "date", "-date"]

	sort = request.GET.get("sort", "-uploaded_at")
	search = request.GET.get("search", "").strip()

	if sort not in VALID_SORT_FIELDS:
		sort = "-uploaded_at"

	tables = UploadedTable.objects.filter(user=request.user)

	if search:
		tables = tables.filter(
			Q(title__icontains=search))

	tables = tables.order_by(sort)

	paginator = Paginator(tables, 9)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)


	user_settings = UserSettings.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)

	return render(request, 'history/index.html', {"search": search, "sort": sort, "page_obj": page_obj, 'dark': user_settings.darkMode, 'profile_picture':  user_profile.profile_picture if user_profile and user_profile.profile_picture else None})


@login_required
# Create your views here.
def view_cells(request, table_id):
	# Fetch the selected table
	table = get_object_or_404(UploadedTable, id=table_id)
	user_settings = UserSettings.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)
	# Fetch all cells related to this table
	cells = TableCell.objects.filter(table=table)
	max_column_index = cells.aggregate(Max('column_number'))['column_number__max']

	calendar_form = CalendarForm()


	return render(request, 'history/view_cells.html', {"calendar_form":calendar_form, "columns": max_column_index + 1, 'table': table, 'cells': cells, 'dark': user_settings.darkMode, 'profile_picture':  user_profile.profile_picture if user_profile and user_profile.profile_picture else None})


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

		saveToCalendar = UserSettings.objects.get(user=request.user).saveToCalendar
		if saveToCalendar and action == 'convert+':
			action="convert"
			calendar = get_object_or_404(LocalCalendar, slug="shifts-calendar")

			# Save the event to the database
			event = LocalEvent.objects.create(
				title=name,
				start=start_datetime,
				end=end_datetime,
				creator=request.user,  # Use the logged-in user as the event creator
				calendar=calendar  # Or your default calendar
			)

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
