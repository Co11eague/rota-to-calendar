from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(
		max_length=150,
		widget=forms.TextInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'username'
		})
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': '••••••••'
		})
	)
