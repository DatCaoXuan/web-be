from django.contrib import admin

from .models import Order, OrderItem

class OrderItemAdmin(admin.StackedInline):
	model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'created_at', 'view_items', ] 
	inlines = (OrderItemAdmin, )

	@admin.display(empty_value='No items', description='Items')
	def view_items(self, obj):
		return ', '.join([i.book.title for i in obj.items.all() if i.book])
