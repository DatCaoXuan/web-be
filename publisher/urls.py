from django.urls import path

from .views import PublisherViewSet

urlpatterns = [
	path('', PublisherViewSet.as_view({
		'get': 'get_publishers'
	}), name='publishers'),
	path('<int:id>/', PublisherViewSet.as_view({
		'get': 'get_publisher'
	}), name='publisher'),
]
