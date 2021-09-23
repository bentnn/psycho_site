from django.db import models
from django.contrib.auth.models import Group, User
import datetime


class Test1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    audio = models.IntegerField()
    visual = models.IntegerField()
    kinest = models.IntegerField()
    date = models.DateField(default=datetime.date(2021, 7, 20))


class Test2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    rt = models.IntegerField()
    lt = models.IntegerField()
    date = models.DateField(default=datetime.date(2021, 7, 20))


class Test3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    ud = models.IntegerField()
    date = models.DateField(default=datetime.date(2021, 7, 20))


class Test4(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    activity = models.IntegerField()
    being = models.IntegerField()
    mood = models.IntegerField()
    date = models.DateField(default=datetime.date(2021, 7, 20))

class Test5(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    sincerity = models.IntegerField()
    extrav = models.IntegerField()
    neuro = models.IntegerField()
    date = models.DateField(default=datetime.date(2021, 7, 20))
