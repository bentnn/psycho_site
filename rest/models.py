from django.db import models
from django.contrib.auth.models import User


class UserTelegramID(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    telegram_id = models.IntegerField(unique=True)
