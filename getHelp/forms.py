from django import forms


class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(widget=forms.Textarea, required=True)


class FineTuneForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(widget=forms.Textarea, required=True)
	file = forms.FileField(required=True)