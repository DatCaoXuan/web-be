from django.db import models
from book.models import Book
from authentication.models import User

class Order(models.Model):

	user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=300)
	address = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	phone_number = models.CharField(max_length=12)
	credit_card = models.CharField(max_length=16)

class OrderItem(models.Model):

	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, related_name='order_items', null=True)
	is_physical = models.BooleanField()
	amount = models.PositiveIntegerField()

