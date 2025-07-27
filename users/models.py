from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


# Wallet model connected to User
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user.username}"


class Invoice(models.Model):
    """Model for storing invoice details"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_address = models.CharField(max_length=255, blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Invoice for {self.user.username}"