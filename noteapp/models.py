from django.db import models

from registerapp.models import UserRegistration


# Create your models here.

class Label(models.Model):
    label_name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)


class Note(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField()
    user = models.ForeignKey(UserRegistration, related_name='+', on_delete=models.CASCADE)
    label_name = models.ManyToManyField(Label, default=None, related_name='note_label')
    collaborator = models.ManyToManyField(UserRegistration, related_name='collab')


