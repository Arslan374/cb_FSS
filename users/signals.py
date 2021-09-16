from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from .models import Profile
from cloud.models import Folder


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        folder = Folder.objects.create(
            user=instance, name='Home',)
        folder.save()
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
