from django.db import models


class Genre(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=999, blank=True)

	def __str__(self) -> str:
		return self.name
