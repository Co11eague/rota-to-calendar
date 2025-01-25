from django import forms

from conversion.models import UploadedTable


class ConversionForm(forms.ModelForm):
	class Meta:
		model = UploadedTable

		fields = ["image", "column_count"]

		widgets = {
			'image': forms.FileInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'accept': 'image/*'
			}),
			'column_count': forms.NumberInput(attrs={
				'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-300 dark:focus:ring-blue-500 dark:focus:border-blue-500',
				'min': 1,
				'max': 100
			}),		}
