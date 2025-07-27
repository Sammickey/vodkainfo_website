from telegram import Bot   
import os
from telegram.error import RetryAfter,Forbidden, TimedOut
from celery import shared_task  
import time
from asgiref.sync import async_to_sync
from django.conf import settings

from dashboard.models import StatusChoices, Price
from dashboard.utils import make_lookup_request
from users.models import Wallet, Invoice

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_ADMIN_ID = settings.TELEGRAM_ADMIN_ID

@shared_task
def debug_add(x, y):
    """A simple task that adds two numbers. for debugging purposes."""
    return x + y

@shared_task
def send_admin_message(message):
    max_retries = 3
    retry_count = 0
    bot = Bot(token=TELEGRAM_BOT_TOKEN )
    while retry_count < max_retries:
        try:
            async_to_sync(bot.send_message)(chat_id=TELEGRAM_ADMIN_ID, text=message)
            return True  # Success
        except RetryAfter as e:
            # Telegram rate limit - wait and retry
            wait_time = e.retry_after
            print(f"Rate limited, waiting {wait_time} seconds")
            time.sleep(wait_time)
            retry_count += 1
        except TimedOut:
            # Connection timed out - retry with backoff
            wait_time = 2 ** retry_count
            print(f"Connection timed out, retrying in {wait_time} seconds")
            time.sleep(wait_time)
            retry_count += 1
        except Forbidden as e:
            print(f"Forbidden Error: {e}")
            return False  # Don't retry on permission errors
        except Exception as e:
            print(f"Error sending message: {e}")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(1)  # Wait before retrying
    
    return False  # Failed after retries


@shared_task
def call_mickeybot_api(user_id, request_model_name, request_id):
    # Dynamically import the model
    from django.apps import apps
    Model = apps.get_model('dashboard', request_model_name)
    request_obj = Model.objects.get(id=request_id)

    # Fetch user wallet
    try:
        wallet = Wallet.objects.get(user_id=user_id)
    except Wallet.DoesNotExist:
        request_obj.status = StatusChoices.FAILED
        request_obj.response = 'No wallet found for user.'
        request_obj.save(update_fields=['response', 'status'])
        return

    # Fetch price for the requested service using model's get_price_field method
    price_obj = Price.objects.last()  # Assuming latest price config
    try:
        price_field = Model.get_price_field()
    except (AttributeError, KeyError):
        request_obj.status = StatusChoices.FAILED
        request_obj.response = f'Price field mapping not found for {request_model_name}.'
        request_obj.save(update_fields=['response', 'status'])
        return
    price = getattr(price_obj, price_field, None)
    if price is None:
        request_obj.status = StatusChoices.FAILED
        request_obj.response = f'Price not set for {request_model_name}.'
        request_obj.save(update_fields=['response', 'status'])
        return

    # Check wallet balance
    if wallet.is_blocked:
        request_obj.status = StatusChoices.FAILED
        request_obj.response = 'Wallet is blocked.'
        request_obj.save(update_fields=['response', 'status'])
        return
    if wallet.balance < price:
        request_obj.status = StatusChoices.FAILED
        request_obj.response = 'Insufficient wallet balance.'
        request_obj.save(update_fields=['response', 'status'])
        return

    # Deduct price from wallet
    wallet.balance -= price
    wallet.save(update_fields=['balance'])

    # Create invoice
    invoice = Invoice.objects.create(
        user_id=user_id,
        btc_address='',  # Fill if needed
        amount_usd=price,
        currency='USD',
        payment_status='paid',
        expires_at=request_obj.created_at  # Or set as needed
    )

    # Set status to processing
    request_obj.status = StatusChoices.PROCESSING
    request_obj.save(update_fields=['status'])

    # Prepare API call
    endpoint = Model.ENDPOINT
    data = request_obj.to_dict()
    response = async_to_sync(make_lookup_request)(endpoint, data)

    if response is not None and response.get('response') is not None:
        request_obj.status = StatusChoices.SUCCESS
        request_obj.response = response['response']
        request_obj.save(update_fields=['response', 'status'])
    else:
        # Refund the price to the wallet
        wallet.balance += price
        wallet.save(update_fields=['balance'])
        # Update invoice status to failed/refunded
        invoice.payment_status = 'failed'
        invoice.save(update_fields=['payment_status'])
        request_obj.status = StatusChoices.FAILED
        request_obj.save(update_fields=['response', 'status'])