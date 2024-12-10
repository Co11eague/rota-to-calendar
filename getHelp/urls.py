from django.urls import path

from getHelp.views import index

urlpatterns = [
	path('', index, name='getHelp'),
]