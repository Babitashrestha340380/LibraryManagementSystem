from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Member

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Member profile when a new User is created.
    """
    if created and not instance.is_staff:  # Only for non-admin users
        Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_member_profile(sender, instance, **kwargs):
    """
    Ensures the Member profile is saved when the User is saved.
    """
    if hasattr(instance, 'member'):
        instance.member.save()
