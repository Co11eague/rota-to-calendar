from django.shortcuts import render
def index(request):
	return render(request, 'signin/index.html')
# Create your views here.
