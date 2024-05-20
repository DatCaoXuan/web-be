from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ['title', 'book_type', 'view_authors', 'publisher']
	prepopulated_fields = {"slug": ("title",)} 

	@admin.display(empty_value='No author', description='Authors')
	def view_authors(self, obj):
		return ', '.join([a.name for a in obj.authors.all()])
