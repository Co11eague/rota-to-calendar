from django import forms

from getHelp.models import Contact


class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['name', 'email', 'message', 'file', 'helpType']

		OPTIONS = [
			('general', 'General Help'),
			('fine-tuning', 'Fine-tuning Help'),
		]

		widgets = {
			'name': forms.TextInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': 'name'
			}),
			'email': forms.EmailInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': 'email'
			}),
			'message': forms.Textarea(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': 'message'
			}),
			'helpType': forms.RadioSelect(attrs={
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
			}),
			'file': forms.FileInput(attrs={})


		}