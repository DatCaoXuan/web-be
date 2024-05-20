from django.urls import path

from .views import GenreViewSet

urlpatterns = [
	path('', GenreViewSet.as_view({
		'get': 'get_genres'
	}), name='genres'),
	path('<int:id>/', GenreViewSet.as_view({
		'get': 'get_genre'
	}), name='genre'),
]

