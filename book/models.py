from django.db import models
from django.template.defaultfilters import slugify

from author.models import Author
from publisher.models import Publisher
from genre.models import Genre

class BookType(models.IntegerChoices):
	BOTH = 0, 'Both'
	PHYSICAL = 1, 'Physical'
	EBOOK = 2, 'E-book'

def upload_to(instance, filename):
	return f'images/thumbnails/{filename}'

class Book(models.Model):
	image_url = models.CharField(max_length=500, blank=True, null=True)
	title = models.CharField(max_length=200)
	slug = models.SlugField(null=True, max_length=400, unique=True)
	description = models.CharField(max_length=999, blank=True)
	pageCount = models.PositiveIntegerField(default=0)
	price = models.PositiveIntegerField(default=0)
	publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
	published_date = models.DateField(null=True)
	authors = models.ManyToManyField(Author, related_name='books')
	book_type = models.PositiveIntegerField(choices=BookType.choices, default=BookType.BOTH)
	link = models.CharField(max_length=500, null=True, blank=True)
	amount_in_stock = models.PositiveIntegerField(null=True, blank=True)
	genres = models.ManyToManyField(Genre, related_name='books')

	def __str__(self) -> str:
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)
