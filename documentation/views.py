from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings


@login_required
def index(request):
	if request.user.is_authenticated:
		user_settings = UserSettings.objects.get(user=request.user)
		dark = user_settings.darkMode
		user_profile = UserProfile.objects.get(user=request.user)
	else:
		dark = False
		user_profile = None

	return render(request, 'documentation/index.html', {'dark': dark,
	                                                    'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})
# Create your views here.
