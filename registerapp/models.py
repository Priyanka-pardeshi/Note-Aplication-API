from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    contact = models.CharField(max_length=12)
    dob = models.DateField()


