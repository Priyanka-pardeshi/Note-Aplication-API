from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserRegistration(AbstractUser):
    bio = models.TextField(null=True)
    location = models.CharField(max_length=12, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    is_verify = models.BooleanField(default=False)

