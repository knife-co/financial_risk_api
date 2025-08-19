# financial/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FinancialProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_financial_profile(sender, instance, created, **kwargs):
    """
    Automatically create a FinancialProfile when a User is created
    """
    if created:
        FinancialProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_financial_profile(sender, instance, **kwargs):
    """
    Ensure the FinancialProfile is saved when User is saved
    """
    if hasattr(instance, 'financial_profile'):
        instance.financial_profile.save()