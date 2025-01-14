from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from getHelp.forms import ContactForm
from getHelp.models import Contact


@login_required
def index(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			Contact.objects.create(
				name=form.cleaned_data['name'],
				email=form.cleaned_data['email'],
				message=form.cleaned_data['message']
			)
			messages.success(request, 'Your message has been sent successfully!')
			return redirect('home')
		else:
			print(form.errors)
	else:
		form = ContactForm()
	return render(request, 'getHelp/index.html', {'form': form})
