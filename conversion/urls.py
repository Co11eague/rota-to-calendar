from django.urls import path

from conversion.views import index

urlpatterns = [
	path('', index, name='conversion'),

]