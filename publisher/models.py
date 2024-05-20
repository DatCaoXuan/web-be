from django.db import models

class Publisher(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=255, blank=True)
	hotline = models.CharField(max_length=12, blank=True)

	def __str__(self) -> str:
		return self.name
	
