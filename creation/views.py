from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from schedule.models import Calendar
from schedule.models import Event

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings
from creation.forms import EventForm


@login_required
def index(request):
	user_settings = UserSettings.objects.get(user=request.user)
	user_profile = UserProfile.objects.get(user=request.user)
	event_form = EventForm()
	return render(request, 'creation/index.html', {'event_form': event_form, 'dark': user_settings.darkMode,
	                                               'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})


def user_events(request):
	if request.user.is_authenticated:
		# Filter events where the creator is the logged-in user
		events = Event.objects.filter(creator=request.user)
		events_data = [{"title": event.title, "start": event.start, "end": event.end, "description": event.description} for event in events]
		return JsonResponse(events_data, safe=False)
	return JsonResponse([], safe=False)


def add_event(request):
	if request.method == 'POST' and request.user.is_authenticated:
		event_form = EventForm(request.POST)

		if event_form.is_valid():
			event = event_form.save(commit=False)

			calendar = get_object_or_404(Calendar, slug="shifts-calendar")

			event.creator = request.user
			event.calendar = calendar
			event.save()

			messages.success(request, 'Your shift was successfully added!')
		else:
			messages.error(request, 'There was an input issue adding your shift.')
	return redirect("creation")
