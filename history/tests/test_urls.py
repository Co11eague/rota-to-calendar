from django.test import SimpleTestCase
from django.urls import reverse, resolve
from history.views import index, view_cells, convert



class TestHistoryUrls(SimpleTestCase):
	def test_index_url_resolves(self):
		"""Test if index is returned when url is resolved"""
		url = reverse('history')
		self.assertEqual(resolve(url).func, index)

	def test_view_cells_url_resolves(self):
		"""Test if view_cells is returned when url is resolved"""
		url = reverse('view_cells', args=[1])
		self.assertEqual(resolve(url).func, view_cells)

	def test_convert_url_resolves(self):
		"""Test if convert is returned when url is resolved"""
		url = reverse('convert')
		self.assertEqual(resolve(url).func, convert)