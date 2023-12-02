from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.core.mail import EmailMultiAlternatives, send_mail
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password, validate_username
from rest_framework.authtoken.views import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserRegister(APIView):
	"""POST only View for user registration. Utilizes custom validation function and 
	UserRegistrationSerializer"""

	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		print(request.data)
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			token = Token.objects.get(user = user)
			if user:
				return Response({'user':user.get_username(), 'email':user.email, 'token': token.key}, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	"""POST only view for user login. Utilizes custom email and password validation functions.
	Also utilizes UserLoginSerializer and calls on check_user method of UserLoginSerializer"""

	permission_classes = (permissions.AllowAny,)
	authentication_classes = (TokenAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			token = Token.objects.get(user = user)
			print(token)
			login(request, user)
			return Response({'user':user.get_username(),'email':user.email,'token':token.key}, status=status.HTTP_200_OK)


class UserLogout(APIView):
	"""POST only logout view to logout users. Might be redundant and uneccessary."""

	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	"""GET only view to get user details(email and username). Utilizes UserSerializer"""

	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
	
class ChangePasswordView(APIView):
	"""Change Password view to change user password."""
	
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	
	def post(self, request):
		serializer = ChangePasswordSerializer(data=request.data)
		if serializer.is_valid():
			user = request.user
			if user.check_password(serializer.data.get('old_password')):
				user.set_password(serializer.data.get('new_password'))
				user.save()
				update_session_auth_hash(request, user)
				return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
			return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


		
	
