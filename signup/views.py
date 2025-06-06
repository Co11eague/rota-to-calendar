from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm


def index(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
		else:
			print(form.errors)
	elif request.user.is_authenticated:
		return redirect('home')
	else:
		form = SignupForm()
	return render(request, 'signup/index.html', {'form': form})
