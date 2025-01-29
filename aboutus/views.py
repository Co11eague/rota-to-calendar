from django.shortcuts import render

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings


def index(request):
	if request.user.is_authenticated:
		user_settings = UserSettings.objects.get(user=request.user)
		user_profile = UserProfile.objects.get(user=request.user)
		dark = user_settings.darkMode
	else:
		dark = False
		user_profile = None
	return render(request, 'aboutus/index.html', {'dark': dark, 'profile_picture':  user_profile.profile_picture if user_profile and user_profile.profile_picture else None})
