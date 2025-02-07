from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from accountProfile.models import UserProfile


class CustomPasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(
		label="Old Password",
		widget=forms.PasswordInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': '••••••••'
		})
	)
	new_password1 = forms.CharField(
		label="New Password",
		widget=forms.PasswordInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': '••••••••'
		})
	)
	new_password2 = forms.CharField(
		label="Confirm New Password",
		widget=forms.PasswordInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': '••••••••'
		})
	)


class PersonalDataForm(forms.ModelForm):
	first_name = forms.CharField(
		required=False,
		label='Your first name',
		widget=forms.TextInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'name'
		})
	)
	last_name = forms.CharField(
		required=False,
		label='Your last name',
		widget=forms.TextInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'surname'
		})
	)
	email = forms.EmailField(
		required=False,
		label='Your email',
		widget=forms.EmailInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'guest@email.com'
		})
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Reorder the fields as desired
		self.fields = {
			'first_name': self.fields['first_name'],
			'last_name': self.fields['last_name'],
			'email': self.fields['email'],
			'date_of_birth': self.fields['date_of_birth'],
			'phone_number': self.fields['phone_number'],
			'address': self.fields['address'],
			'profile_picture': self.fields['profile_picture']
		}

	class Meta:
		model = UserProfile  # Replace with your actual profile model if different
		fields = ['date_of_birth', 'phone_number', 'address', 'profile_picture']  # Include UserProfile fields
		labels = {
			'phone_number': 'Your phone number',
			'address': 'Your address',
			'date_of_birth': 'Your date of birth',
			'profile_picture': 'Your profile picture',
		}
		widgets = {
			'phone_number': forms.TextInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': '+44*********'
			}),
			'address': forms.Textarea(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': '221B Baker Street, London, NW1 6XE, UK',
				'rows': 2
			}),
			'date_of_birth': forms.DateInput(attrs={
				'type': 'date',
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
			}),
			'profile_picture': forms.FileInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'accept': 'image/*'
			})
		}
