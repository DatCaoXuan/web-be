"""
URL configuration for bookstore project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import MediaViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
	path('auth/', include('authentication.urls')),
	path('book/', include('book.urls')),
	path('author/', include('author.urls')),
	path('publisher/', include('publisher.urls')),
	path('genre/', include('genre.urls')),
	path('order/', include('checkout.urls')),
	path('schema/', SpectacularAPIView.as_view(), name='schema'),
	path(f'download', MediaViewSet.as_view({
		'get': 'download'
	}), name='download'),
	path('upload/', MediaViewSet.as_view({
		'post': 'upload'
	}), name='upload'),
	path('', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
