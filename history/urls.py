from django.urls import path

from history.views import index, view_cells, convert

urlpatterns = [
	path('', index, name='history'),
	path('<int:table_id>/cells/', view_cells, name='view_cells'),
	path('calendar-convert/', convert, name='convert'),

]
