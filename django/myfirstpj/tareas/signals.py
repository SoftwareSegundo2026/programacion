from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, created, **kwargs):
    if created:
        return
    profile, _ = Profile.objects.get_or_create(user=instance)
    profile.save()
