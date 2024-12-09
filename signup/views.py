from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm


def index(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # Debug: Show errors in the console
    else:
        form = SignupForm()
    return render(request, 'signup/index.html', {'form': form})
# Create your views here.
