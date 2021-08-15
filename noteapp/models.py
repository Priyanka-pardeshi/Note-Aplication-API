from django.db import models
from registerapp.models import Registration
from registerapp.views import User
# Create your models here.

class Note(models.Model):
    title=models.CharField(max_length=15)
    description=models.TextField()
    register=models.ForeignKey(Registration, on_delete=models.CASCADE)

