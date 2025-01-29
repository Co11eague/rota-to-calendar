# views.py
from django.shortcuts import render

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings
from .models import Slider


def index(request):
	sliders = Slider.objects.all()  # Fetch all slider images
	if request.user.is_authenticated:
		profile_picture = UserProfile.objects.get(user=request.user).profile_picture
		dark = UserSettings.objects.get(user=request.user).darkMode

	else:
		profile_picture = None
		dark = False
	return render(request, 'home/index.html', {'sliders': sliders, 'profile_picture': profile_picture.url, 'dark': dark})
