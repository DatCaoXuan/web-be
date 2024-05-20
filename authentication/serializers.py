from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, User

class LoginSerializer(TokenObtainSerializer):
	token_class = RefreshToken

	def validate(self, attrs):
		data = super().validate(attrs)
		refresh = self.get_token(self.user)

		data["access"] = str(refresh.access_token)
		data['user-id'] = self.user.id
		data['user_role'] = self.user.role

		return data

class UserProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'avatar_url')
		read_only_fields = ('avatar_url', )

class RegisterSerializer(serializers.ModelSerializer):

	profile = UserProfileSerializer()

	class Meta:
		model = User
		fields = ('username', 'password', 'profile')
		extra_kwargs = {'password': {'write_only': True}}

	def validate_password(self, password):
		return make_password(password)

	def create(self, validated_data):
		instance = User.objects.create(username=validated_data.get('username'), password=validated_data.get('password'))
		profile_data = validated_data.pop('profile')
		createdProfile = UserProfile.objects.create(user=instance, **profile_data)
		return instance
