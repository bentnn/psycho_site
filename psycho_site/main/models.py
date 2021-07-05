from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Test1(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    audio = models.IntegerField()
    visual = models.IntegerField()
    kinest = models.IntegerField()