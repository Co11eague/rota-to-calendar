# views.py
from django.shortcuts import render

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings
from .models import Slider


def index(request):
	sliders = Slider.objects.all()  # Fetch all slider images
	if request.user.is_authenticated:
		user_profile = UserProfile.objects.get(user=request.user)
		dark = UserSettings.objects.get(user=request.user).darkMode

	else:
		user_profile = None
		dark = False
	return render(request, 'home/index.html', {'sliders': sliders,
	                                           'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None,
	                                           'dark': dark})
