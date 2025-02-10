from django.urls import path

from creation.views import index, user_events, add_event

urlpatterns = [
	path('', index, name='creation'),
	path('events/', user_events, name='user_events'),
	path('add_event/', add_event, name='add_event'),

]
