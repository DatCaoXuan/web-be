from rest_framework import serializers

from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = OrderItem
		fields = ('book', 'is_physical', 'amount', )

class OrderSerializer(serializers.ModelSerializer):

	items = OrderItemSerializer(many=True)

	class Meta:
		model = Order
		fields = ('id', 'user', 'items', 'name', 'address', 'email', 'phone_number', 'credit_card', )
		read_only_fields = ('created_at', )

	def create(self, validated_data):
		items = validated_data.pop('items', []);

		order = Order.objects.create(**validated_data)
		for item in items:
			OrderItem.objects.create(order=order, **item)

		return order
