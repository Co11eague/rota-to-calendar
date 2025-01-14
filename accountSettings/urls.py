from django.urls import path

from accountSettings.views import index

urlpatterns = [
	path('', index, name='accountSettings'),
]
