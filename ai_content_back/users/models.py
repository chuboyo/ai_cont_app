from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """User model which inherits from Abstract User and has an additional email field"""
    
    email = models.EmailField(unique=True)
