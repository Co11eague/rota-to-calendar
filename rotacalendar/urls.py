"""
URL configuration for rotacalendar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
	              path('admin/', admin.site.urls),
	              path('', include('home.urls')),  # Include the URLs from the 'home' app
	              path('signup/', include('signup.urls')),
	              path('aboutus/', include('aboutus.urls')),
	              path('signin/', include('signin.urls')),
	              path('logout/', LogoutView.as_view(next_page="home"), name='logout'),
	              path('profile/', include('accountProfile.urls')),
	              path('settings/', include('accountSettings.urls')),
	              path('conversion/', include('conversion.urls')),
	              path('creation/', include('creation.urls')),
	              path('documentation/', include('documentation.urls')),
	              path('help/', include('getHelp.urls')),
	              path('history/', include('history.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
