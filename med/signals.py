# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AdminProfile

@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    # Check if the user is a superuser and if a profile already exists
    if instance.is_superuser:
        # Only create a profile if it doesn't already exist
        AdminProfile.objects.get_or_create(user=instance, defaults={'email': instance.email})