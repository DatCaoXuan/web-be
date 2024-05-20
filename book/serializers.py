from rest_framework import serializers
from .models import Book, BookType

class BookSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Book
		fields = ('id', 'title', 'slug', 'image_url', 'price', 'authors', 'book_type', 'genres')
		depth = 1

class BookDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Book
		fields = '__all__'
		depth = 1

class SaveBookSerializer(serializers.ModelSerializer):

	class Meta:
		model = Book
		fields = (
			'image_url', 
			'title', 
			'slug', 
			'description', 
			'pageCount', 
			'price', 
			'publisher', 
			'published_date', 
			'authors', 
			'book_type', 
			'link', 
			'amount_in_stock', 
			'genres'
		)

	def validate(self, data):
		book_type = data.get('book_type')
		link = data.get('link')

		if book_type == BookType.EBOOK and link == None:
			raise serializers.ValidationError('link is required for e-book')
		
		return super().validate(data)

class BookFileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ('link', )
