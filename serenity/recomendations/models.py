from django.db import models

# Create your models here.
from django.conf import settings


class UserIntrests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_intrests')
    text = models.CharField(max_length=1000)


class UserGenre(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_gener')
    name = models.CharField(max_length=255)
