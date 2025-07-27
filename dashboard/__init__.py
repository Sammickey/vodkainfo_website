
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from decimal import Decimal


def ensure_price_instance():
    from dashboard.models import Price

    if not Price.objects.exists():
        Price.objects.create()

@receiver(post_migrate)
def post_migrate_handler(sender, **kwargs):
    ensure_price_instance()
