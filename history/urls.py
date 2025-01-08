from django.urls import path

from history.views import index, view_cells

urlpatterns = [
	path('', index, name='history'),
	path('history/<int:table_id>/cells/', view_cells, name='view_cells'),

]