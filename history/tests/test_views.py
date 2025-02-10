from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from schedule.models import Calendar

from accountSettings.models import UserSettings
from conversion.models import UploadedTable, TableCell


class HistoryViewsTest(TestCase):
	def setUp(self):
		self.dummy_table_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
		self.dummy_cell_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")


		self.client = Client()
		self.user = User.objects.create_user(username='testuser', email='tester@test.com', password='testing123*')
		self.calendar = Calendar.objects.create(name="Shifts Calendar", slug="shifts-calendar")
		self.table = UploadedTable.objects.create(
			user=self.user,
			title="Test Table",
			image=self.dummy_table_image
		)
		self.cell = TableCell.objects.create(
			table=self.table,
			image=self.dummy_cell_image,
			column_number=1,
			row_number=1,
			ocr_text="Sample Text"
		)
	def test_index_requires_login(self):
		"""Ensure unauthenticated users are redirected."""
		response = self.client.get(reverse('history'))
		self.assertEqual(response.status_code, 302)

	def test_index_valid_request(self):
		"""Check if authenticated user gets a valid response."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.get(reverse('history'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'history/index.html')

	def test_view_cells_valid(self):
		"""Test viewing a valid table's cells."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.get(reverse('view_cells', args=[self.table.id]))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'history/view_cells.html')

	def test_view_cells_invalid(self):
		"""Test that an invalid table ID gives a 404 error."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.get(reverse('view_cells', args=[99999]))  # Non-existent table
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("home"))
		messages = list(get_messages(response.wsgi_request))
		self.assertTrue(
			any(msg.message == "The requested table does not exist." and msg.level_tag == "error" for msg in messages))

	@patch('history.views.LocalEvent.objects.create')  # Mock DB Event creation
	def test_convert_valid_form(self, mock_event_create):
		"""Test successful form submission results in .ics file download."""
		self.client.login(username='testuser', password='testing123*')
		data = {
			'title': 'Meeting',
			'location': 'Office',
			'start_date': '2025-02-10',
			'end_date': '2025-02-10',
			'start_time': '10:00',
			'end_time': '12:00',
			'action': 'convert',
		}
		response = self.client.post(reverse('convert'), data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'text/calendar')