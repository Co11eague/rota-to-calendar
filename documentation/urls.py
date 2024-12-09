from django.urls import path

from documentation.views import index

urlpatterns = [
	path('', index, name='documentation'),
]