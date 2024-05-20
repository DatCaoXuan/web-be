from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bookstore.utils import APICode

from .models import Author
from .serializers import AuthorSerializer

class AuthorViewSet(ViewSet):
	serializer_class = AuthorSerializer
	permission_classes = [AllowAny, ]

	def get_authors(self, request):
		authors = Author.objects.all()
		serializer = AuthorSerializer(authors, many=True)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived {len(authors)} author(s)',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	def get_author(self, request, id):
		author = Author.objects.get(pk=id)
		serializer = AuthorSerializer(author)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived author',
			'data': serializer.data
		}, status=status.HTTP_200_OK)