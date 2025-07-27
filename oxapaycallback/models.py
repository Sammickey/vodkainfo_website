from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class OxapayInvoice(models.Model):
    """Model for storing invoice details"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_address = models.CharField(max_length=255, blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    CURRENCY_CHOICES = [
        ('BTC', 'BTC'),
        ('LTC', 'LTC'),
        ('ETH', 'ETH'),
        ('TRC20', 'TRC20'),
        ('ERC20', 'ERC20'),
    ]
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Invoice for {self.user.username}"