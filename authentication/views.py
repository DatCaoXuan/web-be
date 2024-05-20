from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from bookstore.utils import APICode
from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer
from .models import User

class LoginView(TokenObtainPairView):
	permission_classes = (AllowAny, )
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid()
		except Exception:
			return Response({
				'code': APICode.INVALID_LOGIN,
				'message': 'Invalid login info',
			}, status=status.HTTP_401_UNAUTHORIZED)

		return Response({
			'code': APICode.LOGIN_SUCCESS,
            'message': 'User authenticated',
            'data': serializer.validated_data,
		}, status=status.HTTP_200_OK)
	
class RegisterView(APIView):
	serializer_class = RegisterSerializer
	permission_classes = (AllowAny, )

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.save()

			return Response({
				'code': APICode.REGISTER_SUCCESS,
				'message': f'Created user',
				'data': serializer.data
			}, status=status.HTTP_201_CREATED)
		else:
			print(serializer.errors)

		return Response({
			'code': APICode.REGISTER_FAIL,
			'message': 'Request failed',
		}, status=status.HTTP_400_BAD_REQUEST)
	
class ProfileView(APIView):
	serializer_class = UserProfileSerializer
	permission_classes = (AllowAny, )

	def get(self, request, id):
		user = User.objects.get(pk=id)
		serializer = UserProfileSerializer(user.profile)
		return Response({
			'code': APICode.DATA_FETCHED,
			'message': f'Retrived profile',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
