from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserProfile

class UserProfileAdmin(admin.StackedInline):
	model = UserProfile

class UserAdmin(admin.ModelAdmin):
	inlines = (UserProfileAdmin, )
    
admin.site.register(User, UserAdmin)
