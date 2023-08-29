from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.views import Token
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	"""User registration serializer that exposes fields on user model for user registration"""

	class Meta:
		model = UserModel
		fields = ['username', 'email', 'password']
		extra_kwargs = {'password': {
            'write_only': True,
            'required': True,
        }}
		
	# modified create method to use cleaned data to create user and generate authentication token on 
	# user creation.
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(username=clean_data['username'], email=clean_data['email'], password=clean_data['password'])
		user_obj.save()
		Token.objects.create(user=user_obj)
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	"""Login serializer to collect email and password fields for login"""

	email = serializers.EmailField()
	password = serializers.CharField()
	
	#custom method to authenticate user on login
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user
	

class UserSerializer(serializers.ModelSerializer):
	"""User serializer to expose email and username field for user management page"""
	class Meta:
		model = UserModel
		fields = ('email', 'username')
		
class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer to collect old password and new password for password modification"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    """Reset password serializer to collect email for password reset"""

    email = serializers.EmailField(required=True)