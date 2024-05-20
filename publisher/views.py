from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bookstore.utils import APICode

from .models import Publisher
from .serializers import PublisherSerializer


class PublisherViewSet(ViewSet):
	serializer_class = PublisherSerializer
	permission_classes = [AllowAny, ]

	def get_publishers(self, request):
		pubs = Publisher.objects.all()
		serializer = PublisherSerializer(pubs, many=True)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived {len(pubs)} publisher(s)',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	
	def get_publisher(self, request, id):
		pub = Publisher.objects.get(pk=id)
		serializer = PublisherSerializer(pub)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived publisher',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
