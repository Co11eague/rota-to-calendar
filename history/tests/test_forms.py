from datetime import date, time

from django.test import TestCase

from history.forms import CalendarForm


class CalendarFormTest(TestCase):
	def test_valid_form(self):
		"""Test a fully valid form submission."""
		form_data = {
			'title': 'July shift',
			'location': 'Wetherspoons',
			'start_time': time(9, 0),
			'end_time': time(17, 0),
			'start_date': date(2025, 7, 1),
			'end_date': date(2025, 7, 31)
		}
		form = CalendarForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		form = CalendarForm(data={})

		self.assertFalse(form.is_valid())
		expected_fields = {'title', 'location', 'start_time', 'end_time', 'start_date', 'end_date'}
		self.assertTrue(expected_fields.issubset(set(form.errors.keys())))

	def test_invalid_start_end_time_form(self):
		form_data = {
			'title': 'July shift',
			'location': 'Wetherspoons',
			'start_time': "25:00",
			'end_time': "random",
			'start_date': date(2025, 7, 1),
			'end_date': date(2025, 7, 31)
		}

		form = CalendarForm(data=form_data)

		self.assertFalse(form.is_valid())
		expected_fields = {'start_time', 'end_time'}
		self.assertTrue(expected_fields.issubset(set(form.errors.keys())))

	def test_invalid_start_end_date_form(self):
		form_data = {
			'title': 'July shift',
			'location': 'Wetherspoons',
			'start_time': time(9, 0),
			'end_time': time(17, 0),
			'start_date': "random",
			'end_date': "07-31-2025"
		}

		form = CalendarForm(data=form_data)

		self.assertFalse(form.is_valid())
		expected_fields = {'start_date', 'end_date'}
		self.assertTrue(expected_fields.issubset(set(form.errors.keys())))