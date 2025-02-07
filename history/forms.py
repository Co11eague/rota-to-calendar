from django import forms


class CalendarForm(forms.Form):
	title = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'July shift',
			'id': 'title-input'
		})
	)
	location = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'placeholder': 'Wetherspoons',
			'id': 'location-input'
		})
	)
	start_time = forms.TimeField(
		widget=forms.TimeInput(attrs={
			'type': 'time',
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'id': 'start-time-input'
		})
	)
	end_time = forms.TimeField(
		widget=forms.TimeInput(attrs={
			'type': 'time',
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'id': 'end-time-input'
		})
	)
	start_date = forms.DateField(
		widget=forms.DateInput(attrs={
			'type': 'date',
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'id': 'start-date-input'
		})
	)
	end_date = forms.DateField(
		widget=forms.DateInput(attrs={
			'type': 'date',
			'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
			'id': 'end-date-input'
		})
	)
