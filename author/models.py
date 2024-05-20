from django.db import models


class Author(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=255)

	def __str__(self) -> str:
		return self.name
