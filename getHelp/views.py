from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from getHelp.forms import ContactForm
from getHelp.models import Contact


def index(request):
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
				form.save()
				messages.success(request, 'Your message has been sent successfully!')
				return redirect('home')
		else:
			print(form.errors)
	else:
		form = ContactForm()
	return render(request, 'getHelp/index.html', {'form': form})
