from os.path import pathsep

from django.urls import path

from creation.views import index

urlpatterns = [
	path('', index, name='creation'),
]