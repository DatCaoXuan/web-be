from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class UserRole(models.IntegerChoices):
	CUSTOMER = 0, 'Customer'
	ADMIN = 1, 'Admin'

class User(AbstractUser):
	
	username = models.CharField("username", max_length=150, unique=True)
	is_active = models.BooleanField("active", default=True)
	role = models.PositiveIntegerField("role", choices=UserRole.choices, default=UserRole.CUSTOMER)
	date_joined = models.DateTimeField("date joined", default=timezone.now)

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username
	
	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True
	
def upload_to(instance, filename):
	return f'images/{filename}'

class UserProfile(models.Model):

	user = models.OneToOneField('User', verbose_name='user', related_name='profile', on_delete=models.CASCADE, null=True)
	avatar_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
	first_name = models.CharField(max_length=150, blank=True)
	last_name = models.CharField(max_length=150, blank=True)
	email = models.EmailField(max_length=255)
	phone_number = models.CharField(max_length=12, blank=True)
	address = models.CharField(max_length=255, blank=True)

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name
