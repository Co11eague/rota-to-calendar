from django import forms

from accountSettings.models import UserSettings


class SettingsForm(forms.ModelForm):
	class Meta:
		model = UserSettings
		fields = ['darkMode', 'ocrRecognition', 'saveToCalendar']  # Include UserProfile fields

		OPTIONS = [
			('native', 'Native OCR'),
			('easyocr', 'EasyOCR'),
		]

		widgets = {
			'darkMode': forms.CheckboxInput(attrs={
				'class': 'sr-only peer',
				'placeholder': 'Dark Mode'
			}),
			'ocrRecognition': forms.Select(attrs={
				'class': 'text-sm text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md p-1',
			}),
			'saveToCalendar': forms.CheckboxInput(attrs={
				'class': 'sr-only peer',
			})
		}


