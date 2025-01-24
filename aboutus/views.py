from django.shortcuts import render

from accountSettings.models import UserSettings


def index(request):
	if request.user.is_authenticated:
		user_settings = UserSettings.objects.get(user=request.user)
		dark = user_settings.darkMode
	else:
		dark = False
	return render(request, 'aboutus/index.html', {'dark': dark})
