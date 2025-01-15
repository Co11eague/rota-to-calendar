from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from accountProfile.models import UserProfile


class CustomPasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(
		label="Old Password",
		widget=forms.PasswordInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Enter your old password'
		})
	)
	new_password1 = forms.CharField(
		label="New Password",
		widget=forms.PasswordInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Enter your new password'
		})
	)
	new_password2 = forms.CharField(
		label="Confirm New Password",
		widget=forms.PasswordInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Confirm your new password'
		})
	)


class PersonalDataForm(forms.ModelForm):
	first_name = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Enter your first name'
		})
	)
	last_name = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Enter your last name'
		})
	)
	email = forms.EmailField(
		required=False,
		widget=forms.EmailInput(attrs={
			'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			'placeholder': 'Enter your email'
		})
	)

	class Meta:
		model = UserProfile  # Replace with your actual profile model if different
		fields = ['date_of_birth', 'phone_number', 'address', 'profile_picture']  # Include UserProfile fields
		widgets = {
			'phone_number': forms.TextInput(attrs={
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
				'placeholder': 'Enter your phone number'
			}),
			'address': forms.Textarea(attrs={
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
				'placeholder': 'Enter your address',
				'rows': 3
			}),
			'date_of_birth': forms.DateInput(attrs={
				'type': 'date',
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			}),
			'profile_picture': forms.ClearableFileInput(attrs={
				'class': 'mt-1 block w-full text-blue-600',
				'accept': 'image/*'
			})
		}
