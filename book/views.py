from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from bookstore.utils import APICode

from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookDetailsSerializer, BookSerializer, SaveBookSerializer, BookFileSerializer
from .filters import BookFilter
from django.conf import settings


class BookViewSet(ViewSet):
	serializer_class = BookDetailsSerializer
	permission_classes = [AllowAny, ]
	permission_classes_by_action = {
		('get_books', 'get_book'): AllowAny,
		('create_book', 'update_book'): IsAuthenticated,
	}
	queryset = Book.objects.all()
	filter_backends = (DjangoFilterBackend, )
	search_fields = ('title', 'slug',)
	filterset_class = BookFilter

	def get_queryset(self):
		return self.queryset

	def get_permissions(self):
		try:
			return [v() for k, v in self.permission_classes_by_action.items() if self.action in k]
		except KeyError:
			return [_() for _ in self.permission_classes]
	
	def filter_queryset(self, queryset):
		for backend in list(self.filter_backends):
			queryset = backend().filter_queryset(self.request, queryset, self)
		return queryset

	@extend_schema(
		summary='Get all books', 
		responses=BookSerializer, 
		parameters=[
			OpenApiParameter(name='search', description='Search keyword for title or slug', type=str),
			OpenApiParameter(name='author', description='Search keyword for author name', type=str),
			OpenApiParameter(name='genres', description='Genre IDs (seperated by commas)', type=str),
			OpenApiParameter(name='book_type', description='Book type', type=int),
			OpenApiParameter(name='start', description='Offset from the start', type=int),
			OpenApiParameter(name='limit', description='Number of results to be return', type=int),
		]
	)
	def get_books(self, request):

		books = self.filter_queryset(self.get_queryset())
		serializer = BookSerializer(books, many=True)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived {len(books)} book(s)',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	@extend_schema(summary='Get a book')
	def get_book(self, request, id):
		book = Book.objects.get(pk=id)
		serializer = BookDetailsSerializer(book)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived book',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	@extend_schema(summary='Get a book by slug')
	def get_book_by_slug(self, request, slug):
		book = Book.objects.get(slug=slug)
		serializer = BookDetailsSerializer(book)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived book',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	@extend_schema(summary='Create a book', responses=SaveBookSerializer)
	def create_book(self, request):
		serializer = SaveBookSerializer(data=request.data)

		if serializer.is_valid():
			created = serializer.save()

			return Response({
				'code': APICode.RESOURCE_CREATED,
				'message': f'Created book',
				'data': BookDetailsSerializer(created).data
			}, status=status.HTTP_201_CREATED)
		else:
			print(serializer.errors)

		return Response({
			'code': APICode.REQUEST_FAIL,
			'message': 'Request failed',
		}, status=status.HTTP_400_BAD_REQUEST)
	
	@extend_schema(summary='Update a book', responses=SaveBookSerializer)
	def update_book(self, request, id):
		book = Book.objects.get(pk=id)
		serializer = SaveBookSerializer(book, data=request.data)
		if serializer.is_valid():
			updated = serializer.save()
			return Response({
				'code': APICode.RESOURCE_UPDATED,
				'message': f'Updated book',
				'data': BookDetailsSerializer(updated).data
			}, status=status.HTTP_200_OK)
		else:
			print(serializer.errors)
		
		return Response({
			'code': APICode.REQUEST_FAIL,
			'message': 'Request failed',
		}, status=status.HTTP_400_BAD_REQUEST)

	@extend_schema(summary='Delete a book')
	def delete_book(self, request, id):
		book = Book.objects.get(pk=id)
		book_data = BookDetailsSerializer(book).data
		book.delete()
		
		return Response({
			'code': APICode.RESOURCE_DELETED,
			'message': f'Deleted book',
			'data': book_data,
		}, status=status.HTTP_204_NO_CONTENT)	
