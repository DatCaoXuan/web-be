from django.urls import path

from .views import AuthorViewSet

urlpatterns = [
	path('', AuthorViewSet.as_view({
		'get': 'get_authors'
	}), name='authors'),
	path('<int:id>/', AuthorViewSet.as_view({
		'get': 'get_author'
	}), name='author'),
]
