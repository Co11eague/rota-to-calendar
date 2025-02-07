from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accountProfile.models import UserProfile
from accountSettings.forms import SettingsForm
from accountSettings.models import UserSettings


@login_required
def index(request):
	user = User.objects.get(id=request.user.id)
	userSettings = UserSettings.objects.get(user=user)
	user_profile = UserProfile.objects.get(user=user)

	if request.method == 'POST':
		settings_form = SettingsForm(request.POST, instance=userSettings)
		settings_form.save()
		messages.success(request, 'Your settings were successfully updated!')
		redirect('accountSettings')
	else:
		settings_form = SettingsForm(instance=userSettings)

	return render(request, 'accountSettings/index.html', {'form': settings_form, 'dark': userSettings.darkMode,
	                                                      'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})
# Create your views here.
