import asyncio
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zproject.settings")
django.setup()

from dashboard.utils import make_lookup_request
from dashboard.models import AlexSSN
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

async def main():
    user = await sync_to_async(User.objects.first)()
    obj = AlexSSN(user=user, full_name="John Doe", zip="12345")
    await sync_to_async(obj.save)()  # Save to DB in async context
    endpoint = AlexSSN.ENDPOINT
    data = obj.to_dict()
    response = await make_lookup_request(endpoint, data)
    print("API Response:", response)

if __name__ == "__main__":
    asyncio.run(main())