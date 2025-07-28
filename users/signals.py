# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from users.models import Wallet
# from decimal import Decimal

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_wallet_for_user(sender, instance, created, **kwargs):
#     if created and not hasattr(instance, 'wallet'):
#         if instance.is_superuser:
#             Wallet.objects.create(user=instance, balance=Decimal('1000000.00'), is_blocked=False)
#         else:
#             Wallet.objects.create(user=instance, balance=Decimal('0.00'), is_blocked=False)
