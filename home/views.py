# views.py
from django.shortcuts import render

from .models import Slider


def index(request):
	sliders = Slider.objects.all()  # Fetch all slider images
	return render(request, 'home/index.html', {'sliders': sliders})
