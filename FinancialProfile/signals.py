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

# # financial/signals.py

# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Income, Expense, Debt, Asset, FinancialProfile


# @receiver([post_save, post_delete], sender=Income)
# @receiver([post_save, post_delete], sender=Expense)
# @receiver([post_save, post_delete], sender=Debt)
# @receiver([post_save, post_delete], sender=Asset)
# def auto_create_risk_assessment(sender, instance, **kwargs):
#     """
#     Automatically create a new risk assessment whenever financial data changes
#     """
#     profile = instance.profile
    
#     # Only create assessment if profile has complete data
#     if profile.has_complete_profile():
#         try:
#             # Create new risk assessment
#             assessment = profile.create_risk_assessment()
#             print(f"Auto-created risk assessment: Score {assessment.score} for {profile.user.username}")
#         except Exception as e:
#             print(f"Error creating risk assessment: {e}")


# Alternative: Only create assessment when profile becomes complete
@receiver(post_save, sender=FinancialProfile)
def create_initial_risk_assessment(sender, instance, created, **kwargs):
    """
    Create initial risk assessment when profile is first created
    """
    if created and instance.has_complete_profile():
        try:
            assessment = instance.create_risk_assessment()
            print(f"Created initial risk assessment for {instance.user.username}")
        except Exception as e:
            print(f"Error creating initial risk assessment: {e}")