from datetime import datetime
from unittest import mock
from unittest.mock import patch, ANY, MagicMock

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from schedule.models import Calendar
from schedule.models import Event as LocalEvent


from accountSettings.models import UserSettings
from conversion.models import UploadedTable, TableCell
from history.views import index, view_cells, convert


class HistoryViewsUnitTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testuser', email='tester@test.com', password='testing123*')
		self.user_settings = mock.MagicMock(spec=UserSettings)
		self.user_settings.darkMode = True

	@patch("history.views.UploadedTable.objects.filter")
	@patch("history.views.UserSettings.objects.get")
	@patch("history.views.UserProfile.objects.get")
	def test_index_view(self, mock_user_profile, mock_user_settings, mock_uploaded_table_filter):
		"""Test index view with mocked database calls."""
		request = self.factory.get(reverse("history"))
		request.user = self.user

		mock_user_settings.return_value = self.user_settings
		mock_user_profile.return_value.profile_picture = None
		mock_uploaded_table_filter.return_value.order_by.return_value = []

		response = index(request)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"search", response.content)

	@patch("history.views.UserSettings.objects.get")
	@patch("history.views.LocalEvent.objects.create")
	@patch("history.views.get_object_or_404")
	def test_convert_saves_to_calendar(self, mock_get_calendar, mock_local_event_create, mock_user_settings_get):
		"""Test convert saves to calendar when enabled."""
		request = self.factory.post(reverse("convert"), data={
			"title": "Meeting",
			"location": "Office",
			"start_date": "2025-02-10",
			"end_date": "2025-02-10",
			"start_time": "10:00",
			"end_time": "12:00",
			"action": "convert"
		})
		request.user = self.user

		mock_user_settings_get.return_value.saveToCalendar = True
		mock_get_calendar.return_value = MagicMock()

		response = convert(request)

		self.assertEqual(response.status_code, 200)
		mock_local_event_create.assert_called_once_with(
			title="Meeting",
			start=ANY,
			end=ANY,
			creator=self.user,
			calendar=mock_get_calendar.return_value
		)

class HistoryViewsIntegrationTest(TestCase):
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

	def test_index_view_sorting_and_search(self):
		"""Test index view with sorting and searching functionality."""
		self.client.login(username="testuser", password="testing123*")

		self.dummy_table_imageA = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
		self.dummy_table_imageB = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")


		UploadedTable.objects.create(user=self.user, title="Test Table A", uploaded_at="2025-02-09", image=self.dummy_table_imageA)
		UploadedTable.objects.create(user=self.user, title="Test Table B", uploaded_at="2025-02-10", image=self.dummy_table_imageB)

		response = self.client.get(reverse('history') + '?sort=-uploaded_at&search=Test')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Test Table A")
		self.assertContains(response, "Test Table B")

	def test_view_cells_valid(self):
		"""Test viewing a valid table's cells."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.get(reverse('view_cells', args=[self.table.id]))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'history/view_cells.html')

	def test_view_cells_invalid(self):
		"""Test that an invalid table ID gives a 404 error."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.get(reverse('view_cells', args=[99999]))
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("home"))
		messages = list(get_messages(response.wsgi_request))
		self.assertTrue(
			any(msg.message == "The requested table does not exist." and msg.level_tag == "error" for msg in messages))

	def test_convert_valid_form(self):
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
		self.assertIn('attachment; filename="Meeting_event.ics"', response['Content-Disposition'])

	def test_convert_invalid_form(self):
		"""Test invalid form submission returns JSON error."""
		self.client.login(username='testuser', password='testing123*')
		response = self.client.post(reverse('convert'), {})
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {'error': "Invalid form data"})

	def test_convert_google_calendar_redirect(self):
		self.client.login(username="testuser", password="testing123*")

		data = {
			'title': 'Meeting',
			'location': 'Office',
			'start_date': '2025-02-10',
			'end_date': '2025-02-10',
			'start_time': '10:00',
			'end_time': '12:00',
			'action': 'google',
		}

		response = self.client.post(reverse('convert'), data)

		self.assertEqual(response.status_code, 302, msg=f"Response didn't redirect: {response.content.decode()}")

		self.assertIn("https://calendar.google.com/calendar/render?", response.url)
		self.assertIn("text=Meeting", response.url)
		self.assertIn("location=Office", response.url)

def test_convert_saves_to_local_calendar(self):
    """Test event is saved to the local calendar when saveToCalendar is enabled."""
    self.client.login(username="testuser", password="testing123*")

    self.user_settings = UserSettings.objects.get(user=self.user)
    self.user_settings.saveToCalendar = True
    self.user_settings.save()

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

    event_exists = LocalEvent.objects.filter(
        title="Meeting",
        location="Office",
        start="2025-02-10 10:00:00",
        end="2025-02-10 12:00:00",
        creator=self.user
    ).exists()

    self.assertTrue(event_exists)

class IndexPaginationTests(TestCase):
    def setUp(self):
        """Create multiple tables for pagination testing."""

        self.dummy_table_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.user = User.objects.create_user(username="testuser", password="testing123*")
        self.client.login(username="testuser", password="testing123*")

        for i in range(15):
            UploadedTable.objects.create(user=self.user, title=f"Table {i+1}", image=self.dummy_table_image)

    def test_pagination_first_page(self):
        """Test first page contains expected number of items."""
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 9)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_pagination_second_page(self):
        """Test second page contains remaining items."""
        response = self.client.get(reverse('history') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertFalse(response.context['page_obj'].has_next())
        self.assertTrue(response.context['page_obj'].has_previous())

    def test_pagination_out_of_range(self):
        """Test accessing a non-existent page returns the last page."""
        response = self.client.get(reverse('history') + '?page=100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_pagination_empty_page(self):
        """Test accessing an empty page defaults to the first page."""
        UploadedTable.objects.all().delete()
        response = self.client.get(reverse('history') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)
