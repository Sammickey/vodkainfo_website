import io
import qrcode
import requests
from django.conf import settings
from django.contrib.auth.models import User
from .models import OxapayInvoice as Invoice
from decimal import Decimal
from django.db import transaction
from users.models import Wallet
from django.utils import timezone
from datetime import timedelta

OXAPAY_API_KEY = settings.OXAPAY_API_KEY

@transaction.atomic
def get_or_update_invoice(btc_address: str, amount: Decimal) -> Wallet | None:
    # Find the invoice by btc_address and payment_status 'pending'
    invoice = (
        Invoice.objects.select_for_update()
        .filter(btc_address=btc_address, payment_status="pending")
        .select_related("user")
        .first()
    )
    if not invoice:
        return None

    # Mark invoice as paid and update amount
    invoice.payment_status = "paid"
    invoice.amount_usd = amount
    invoice.save(update_fields=["payment_status", "amount_usd"])

    # Update user's wallet balance
    wallet = Wallet.objects.select_for_update().get(user=invoice.user)
    wallet.balance += Decimal(str(amount))
    wallet.save(update_fields=["balance"])

    return wallet

def make_qr_code(address: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(address)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def create_oxapay_static_address(currency: str, user: User):
    network = currency
    if currency in ["ERC20", "TRC20"]:
        network = "ERC20" if currency == "ERC20" else "TRC20"
        currency = "USDT"
    body = {
        "currency": currency,
        "network": network,
        "merchant": OXAPAY_API_KEY,
        "callbackUrl": f"{settings.SITE_URL}/oxapaycallback/oxapay/callback/"
    }
    response = requests.post(
        f"https://api.oxapay.com/merchants/request/staticaddress", json=body)
    expires = timezone.now() + timedelta(hours=1)
    default_amount = 0
    default_status = 'pending'

    if response.status_code != 200 or 'address' not in response.json():
        return None

    data = response.json()
    address = data["address"]
    invoice = Invoice.objects.create(
        btc_address=address,
        user=user,
        currency=currency,
        amount_usd=default_amount,
        payment_status=default_status,
        expires_at=expires
    )
    return invoice
