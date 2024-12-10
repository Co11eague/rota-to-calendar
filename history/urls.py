from django.urls import path

from history.views import index

urlpatterns = [
	path('', index, name='history'),
]