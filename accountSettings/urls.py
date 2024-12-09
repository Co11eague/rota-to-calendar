from django.urls import path

from accountProfile.urls import urlpatterns
from accountSettings.views import index

urlpatterns = [
	path('', index, name='accountSettings'),
]