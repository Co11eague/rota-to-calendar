from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from getHelp.forms import ContactForm, FineTuneForm
from getHelp.models import Contact, FineTune


@login_required
def index(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		fineTuneForm = FineTuneForm(request.POST, request.FILES)  # Pass both POST and FILES
		action = request.POST.get('action')
		if action == 'help':
			fineTuneForm = FineTuneForm()
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
			if fineTuneForm.is_valid():
				print("Here")
				FineTune.objects.create(
					name=fineTuneForm.cleaned_data['name'],
					email=fineTuneForm.cleaned_data['email'],
					message=fineTuneForm.cleaned_data['message'],
					file=fineTuneForm.cleaned_data['file']
				)
				messages.success(request, 'Your message has been sent successfully!')
				return redirect('home')
			else:
				print(fineTuneForm.errors)


	else:
		form = ContactForm()
		fineTuneForm = FineTuneForm()
	return render(request, 'getHelp/index.html', {'form': form, 'fineTuneForm': fineTuneForm})
