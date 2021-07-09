from django.db import models
from django.contrib.auth.models import Group, User


class Test1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    audio = models.IntegerField()
    visual = models.IntegerField()
    kinest = models.IntegerField()


class Test2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    rt = models.IntegerField()
    lt = models.IntegerField()

class Test3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    ud = models.IntegerField()
