from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookstore.utils import APICode

from .serializers import OrderSerializer
from .models import Order

class CheckoutViewSet(ViewSet):
	permission_classes = (IsAuthenticated, )
	serializer_class = OrderSerializer
	permission_classes_by_action = {
		('get_orders', 'checkout', ): IsAuthenticated,
	}

	def get_queryset(self):
		return Order.objects.all()
	
	def get_permissions(self):
		try:
			return [v() for k, v in self.permission_classes_by_action.items() if self.action in k]
		except KeyError:
			return [_() for _ in self.permission_classes]

	def get_orders(self, request):
		orders = self.get_queryset()
		serializer = self.serializer_class(orders, many=True)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived {len(orders)} order(s)',
			'data': serializer.data
		}, status=status.HTTP_200_OK)

	def checkout(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			order = serializer.save()

			return Response({
				'code': APICode.RESOURCE_CREATED,
				'message': f'Created order',
				'data': serializer.data
			}, status=status.HTTP_201_CREATED)
		else:
			print(serializer.errors)

		return Response({
			'code': APICode.REQUEST_FAIL,
			'message': 'Request failed',
		}, status=status.HTTP_400_BAD_REQUEST)
