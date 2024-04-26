# models.py

from django.db import models
from django.contrib.auth.models import User

class videoSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, default='default_color')
    fps = models.IntegerField(default=30)

class User_Credentials(models.Model):
    uname = models.CharField(max_length=50)
    pass1 = models.TextField(max_length=25)