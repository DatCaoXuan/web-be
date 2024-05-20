from django.urls import path

from .views import BookViewSet

urlpatterns = [
	path('', BookViewSet.as_view({
		'get': 'get_books',
		'post': 'create_book',
	}), name='books'),
	path('<int:id>/', BookViewSet.as_view({
		'get': 'get_book',
		'put': 'update_book',
		'delete': 'delete_book',
	}), name='book'),
	path('<str:slug>/', BookViewSet.as_view({
		'get': 'get_book_by_slug',
	}), name='book_slug')
]

