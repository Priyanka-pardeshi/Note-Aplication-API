from django.db import models

from registerapp.models import UserRegistration


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField()
    token = models.ForeignKey(UserRegistration, related_name='+', on_delete=models.CASCADE)
