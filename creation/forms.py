from django import forms
from schedule.models import Event


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['title', 'description', 'start', 'end']

		labels = {
			'title': 'Your shift title',
			'description': 'Your shift location',
			'start': 'Your shift start time',
			'end': 'Your shift end time',
		}

		widgets = {
			'title': forms.TextInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': 'title'
			}),
			'description': forms.Textarea(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'placeholder': 'I will be working in...',
				'rows': 3
			}),
			'start': forms.DateTimeInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'type': 'datetime-local',

			}),
			'end': forms.DateTimeInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'type': 'datetime-local',
			})
		}
