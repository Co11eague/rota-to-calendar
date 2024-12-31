from django.urls import path

from conversion import views
from conversion.views import index

urlpatterns = [
	path('', index, name='conversion'),
	path('upload-image/', views.process_table_image, name='process_table_image'),

]