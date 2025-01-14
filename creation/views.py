from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from schedule.models import Calendar
from schedule.models import Event  # Assuming you're using django-scheduler's Event model


@login_required
def index(request):
	return render(request, 'creation/index.html')


# Create your views here.

def user_events(request):
	if request.user.is_authenticated:
		# Filter events where the creator is the logged-in user
		events = Event.objects.filter(creator=request.user)
		events_data = [{"title": event.title, "start": event.start, "end": event.end} for event in events]
		return JsonResponse(events_data, safe=False)
	return JsonResponse([], safe=False)


@csrf_exempt  # Disable CSRF protection for this POST request (in a production app, use a valid CSRF token)
def add_event(request):
	if request.method == 'POST' and request.user.is_authenticated:
		title = request.POST.get('title')
		start_time = request.POST.get('start')
		end_time = request.POST.get('end')

		# Convert start and end times to datetime objects
		start_time = datetime.fromisoformat(start_time)
		end_time = datetime.fromisoformat(end_time)

		calendar = get_object_or_404(Calendar, slug="shifts-calendar")

		# Save the event to the database
		event = Event.objects.create(
			title=title,
			start=start_time,
			end=end_time,
			creator=request.user,  # Use the logged-in user as the event creator
			calendar=calendar  # Or your default calendar
		)
		return JsonResponse({'success': True, 'event_id': event.id})
	return JsonResponse({'success': False}, status=400)
