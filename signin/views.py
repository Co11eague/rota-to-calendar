from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from signin.forms import LoginForm


def index(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			# Authenticate using the custom backend (username or email)
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')  # Redirect to a protected page after login
			else:
				form.add_error(None, 'Invalid login credentials.')
	else:
		form = LoginForm()

	return render(request, 'signin/index.html', {'form': form})
# Create your views here.
