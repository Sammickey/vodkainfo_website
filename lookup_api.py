# import hashlib
# from django.db.models import query
# from telegram import Bot
# import aiohttp
# from typing import Dict, Any, Optional
# from django.conf import settings
# import asyncio
# import uuid
# import hmac
# import urllib.parse
# import time
# import logging

# # Configure logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# if not settings.API_KEY:
#     raise ValueError("API_KEY is not set")

# if not settings.API_BASE_URL:
#     raise ValueError("API_BASE_URL is not set")


# if not settings.TELEGRAM_BOT_TOKEN:
#     raise ValueError("TELEGRAM_BOT_TOKEN is not set")

# bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


# async def send_long_message(bot: Bot, chat_id: int, text: str, max_length: int = 3500) -> None:
#     """
#     Send a long message by splitting it into multiple parts if it exceeds the maximum length.

#     Args:
#         bot: Telegram bot instance
#         chat_id: ID of the chat to send message to
#         text: Message text to send
#         max_length: Maximum length of each message part (default: 4096 for Telegram)
#     """
#     if len(text) <= max_length:
#         await bot.send_message(chat_id, text)
#         return

#     # Split the text into parts
#     parts: list[str] = []
#     while text:
#         if len(text) > max_length:
#             # Find the last newline within the limit
#             split_pos = text.rfind('\n', 0, max_length)
#             if split_pos == -1:
#                 # If no newline found, split at max_length
#                 split_pos = max_length
#             parts.append(text[:split_pos])
#             text = text[split_pos:].lstrip()
#         else:
#             parts.append(text)
#             text = ''

#     # Send each part
#     for part in parts:
#         await bot.send_message(chat_id, part)


# async def make_lookup_request(end_point: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f"Token {settings.API_KEY.strip()}",
#         # 'sandbox': 'True'
#     }
#     try:
#         await send_long_message(bot, settings.TELEGRAM_ADMIN_ID, "Starting API request...full url: " + f"{settings.API_BASE_URL}{end_point}")
#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 f"{settings.API_BASE_URL}{end_point}",
#                 headers=headers,
#                 json=data
#             ) as response:
#                 await send_long_message(bot, settings.TELEGRAM_ADMIN_ID, f"API request status: {response.status} and response: {await response.text()}")
#                 if response.status == 200:
#                     response_json = await response.json()
#                     if response_json.get('response').strip() == '':
#                         return None
#                     return response_json
#                 else:
#                     error_text = await response.text()
#                     logger.error(
#                         f"API request failed with status {response.status}: {error_text}")
#                     return None
#     except Exception as e:
#         logger.error(f"Error making API request: {str(e)}")
#         return None
