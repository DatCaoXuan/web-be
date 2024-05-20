from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bookstore.utils import APICode

from .models import Genre
from .serializers import GenreSerializer

class GenreViewSet(ViewSet):
	serializer_class = GenreSerializer
	permission_classes = [AllowAny, ]

	def get_genres(self, request):
		genres = Genre.objects.all()
		serializer = GenreSerializer(genres, many=True)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived {len(genres)} genre(s)',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	def get_genre(self, request, id):
		genre = Genre.objects.get(pk=id)
		serializer = GenreSerializer(genre)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived genre',
			'data': serializer.data
		}, status=status.HTTP_200_OK)

