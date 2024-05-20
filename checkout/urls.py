from django.urls import path

from .views import CheckoutViewSet

urlpatterns = [
	path('checkout/', CheckoutViewSet.as_view({
		'post': 'checkout',
	}), name='checkout'),
	path('', CheckoutViewSet.as_view({
		'get': 'get_orders',
	}), name='orders')
]

