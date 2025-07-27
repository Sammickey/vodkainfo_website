from django.contrib import admin

from .models import Wallet, Invoice


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['user', 'balance', 'is_blocked', 'created_at']
    list_filter = ['is_blocked']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['user', 'amount_usd', 'currency', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'currency']
