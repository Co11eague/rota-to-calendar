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
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
				'placeholder': 'Dark Mode'
			}),
			'ocrRecognition': forms.RadioSelect(attrs={
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
			}),
			'saveToCalendar': forms.CheckboxInput(attrs={
				'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
			})
		}


