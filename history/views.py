import urllib.parse
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ics import Calendar, Event
from schedule.models import Calendar as LocalCalendar
from schedule.models import Event as LocalEvent

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

	return render(request, 'history/index.html',
	              {"search": search, "sort": sort, "page_obj": page_obj, 'dark': user_settings.darkMode,
	               'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})


@login_required
def view_cells(request, table_id):
	try:
		table = UploadedTable.objects.get(id=table_id)
	except UploadedTable.DoesNotExist:
		messages.error(request, "The requested table does not exist.")
		return redirect("home")

	user_settings = UserSettings.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)

	cells = TableCell.objects.filter(table=table)
	max_column_index = int(table.column_count)

	calendar_form = CalendarForm()

	return render(request, 'history/view_cells.html',
	              {"calendar_form": calendar_form, "columns": max_column_index, 'table': table, 'cells': cells,
	               'dark': user_settings.darkMode,
	               'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})


@csrf_exempt
def convert(request):
	if request.method == 'POST':
		form = CalendarForm(request.POST)

		if form.is_valid():
			action = request.POST.get('action')

			try:
				start_date_str = form.cleaned_data['start_date'].strftime("%Y-%m-%d")
				end_date_str = form.cleaned_data['end_date'].strftime("%Y-%m-%d")
				start_time_str = form.cleaned_data['start_time'].strftime("%H:%M")
				end_time_str = form.cleaned_data['end_time'].strftime("%H:%M")

				start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M")
				end_datetime = datetime.strptime(f"{end_date_str} {end_time_str}", "%Y-%m-%d %H:%M")
			except ValueError:
				start_datetime = None
				end_datetime = None
				messages.error(request, "There was an issue formatting your date for the calendar.")

			if start_datetime and end_datetime:

				saveToCalendar = UserSettings.objects.get(user=request.user).saveToCalendar

				if saveToCalendar and (action == 'convert' or action == 'google') :
					action = "convert"
					calendar = get_object_or_404(LocalCalendar, slug="shifts-calendar")

					LocalEvent.objects.create(
						title=form.cleaned_data['title'],
						start=start_datetime,
						end=end_datetime,
						creator=request.user,
						calendar=calendar
					)
				if action == 'convert' or action == 'convert+':

					c = Calendar()
					e = Event()
					e.name = form.cleaned_data['title']
					e.begin = start_datetime
					e.end = end_datetime
					e.location = form.cleaned_data['location']
					c.events.add(e)

					ics_content = c.serialize()

					response = HttpResponse(ics_content, content_type='text/calendar')
					response[
						'Content-Disposition'] = f'attachment; filename="{form.cleaned_data["title"].replace(" ", "_")}_event.ics"'
					return response
				else:
					google_calendar_url = (
							"https://calendar.google.com/calendar/render?"
							+ urllib.parse.urlencode({
						"action": "TEMPLATE",
						"text": form.cleaned_data['title'],
						"details": f"Event at {form.cleaned_data['location']}",
						"location": form.cleaned_data['location'],
						"dates": f"{start_datetime.strftime('%Y%m%dT%H%M%S')}/{end_datetime.strftime('%Y%m%dT%H%M%S')}",
						"sf": "true",
						"output": "xml"
					})
					)

					# Redirect to Google Calendar
					return redirect(google_calendar_url)
		messages.error(request, "Could not convert event to calendar file.")
		return JsonResponse({'error': "Invalid form data"}, status=400)
