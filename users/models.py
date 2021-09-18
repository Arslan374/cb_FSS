from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def sub_routine():
    return timezone.now() + timedelta(days=30)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    subscription = models.DateTimeField(default=sub_routine)

    def __str__(self) -> str:
        if self.user.username:
            return f'Profile <{self.user.username}>'
        return 'Profile <{self.pk}>'
