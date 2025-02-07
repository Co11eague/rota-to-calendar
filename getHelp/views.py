from django.contrib import messages
from django.shortcuts import render, redirect

from accountProfile.models import UserProfile
from accountSettings.models import UserSettings
from getHelp.forms import ContactForm


def index(request):
	if request.user.is_authenticated:
		user_settings = UserSettings.objects.get(user=request.user)
		dark = user_settings.darkMode
		user_profile = UserProfile.objects.get(user=request.user)
	else:
		dark = False
		user_profile = None
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your message has been sent successfully!')
			return redirect('home')
		else:
			messages.error(request, 'There was something wrong with your input.')
	else:
		form = ContactForm()
	return render(request, 'getHelp/index.html', {'form': form, 'dark': dark,
	                                              'profile_picture': user_profile.profile_picture if user_profile and user_profile.profile_picture else None})
