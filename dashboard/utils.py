import aiohttp
from typing import Dict, Any, Optional
from django.conf import settings
from telegram import Bot
import json


async def send_long_message(bot: Bot, chat_id: int, text: str, max_length: int = 3500) -> None:
    if len(text) <= max_length:
        await bot.send_message(chat_id, text)
        return
    parts: list[str] = []
    while text:
        if len(text) > max_length:
            split_pos = text.rfind('\n', 0, max_length)
            if split_pos == -1:
                split_pos = max_length
            parts.append(text[:split_pos])
            text = text[split_pos:].lstrip()
        else:
            parts.append(text)
            text = ''
    for part in parts:
        await bot.send_message(chat_id, part)

async def make_lookup_request(end_point: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Token {settings.API_KEY.strip()}"
        # 'sandbox': 'True'
    }
    try:
        await send_long_message(bot, settings.TELEGRAM_ADMIN_ID, "Starting API request...full url: " + f"{settings.API_BASE_URL}{end_point} with data: {data}")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.API_BASE_URL}{end_point}",
                headers=headers,
                json=data
            ) as response:
                await send_long_message(bot, settings.TELEGRAM_ADMIN_ID, f"API request status: {response.status} and response: {await response.text()}")
                if response.status == 200:
                    response_json = await response.json()
                    response_data = response_json.get('response')
                    if response_data is None or response_data == '' or (isinstance(response_data, (list, dict)) and len(response_data) == 0):
                        return None
                    return response_json
                else:
                    error_text = await response.text()
                    return None
    except Exception as e:
        logger.error(f"Error making API request: {str(e)}")
        await send_long_message(bot, settings.TELEGRAM_ADMIN_ID, f"Error making API request: {str(e)}")
        return None


def format_string(data: str) -> str:
    # Preprocess: replace single quotes with double quotes for JSON compatibility
    data_cleaned = data.replace("'", '"')
    
    try:
        # Parse the JSON data
        parsed_data = json.loads(data_cleaned)
        
        # Handle case where data might be a list
        if isinstance(parsed_data, list) and len(parsed_data) > 0:
            person_data = parsed_data[0]  # Take first person
        else:
            person_data = parsed_data
        
        output = []
        
        # Function to format any value recursively
        def format_value(value, indent=2):
            if isinstance(value, dict):
                result = []
                for i, (k, v) in enumerate(value.items(), 1):
                    result.append(f"{' ' * indent}Item {i}:")
                    if isinstance(v, (dict, list)):
                        result.extend(format_value(v, indent + 2))
                    else:
                        # Convert key to proper case and format
                        formatted_key = k.replace('_', '').capitalize()
                        result.append(f"{' ' * (indent + 2)}{formatted_key}: {v}")
                return result
            elif isinstance(value, list):
                result = []
                for i, item in enumerate(value, 1):
                    result.append(f"{' ' * indent}Item {i}:")
                    if isinstance(item, (dict, list)):
                        result.extend(format_value(item, indent + 2))
                    else:
                        result.append(f"{' ' * (indent + 2)}{item}")
                return result
            else:
                return [f"{' ' * indent}{value}"]
        
        # Add header separator
        output.append("--------")
        
        # Process each key-value pair in the data
        for key, value in person_data.items():
            # Format the key as a section header
            section_name = key.upper().replace('_', '')
            output.append(f"  {section_name}")
            
            # Add appropriate underline based on length
            underline = "-" * len(section_name)
            output.append(underline)
            
            # Handle the value
            if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                output.append("  No data available.")
            elif isinstance(value, list):
                # Handle lists (like addresses, phones)
                for i, item in enumerate(value, 1):
                    output.append(f"  Item {i}:")
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            formatted_sub_key = sub_key.replace('_', '').capitalize()
                            output.append(f"    {formatted_sub_key}: {sub_value}")
                    else:
                        output.append(f"    {item}")
                    
                    # Add spacing between items except for the last one
                    if i < len(value):
                        output.append("")
            elif isinstance(value, dict):
                # Handle nested dictionaries
                for sub_key, sub_value in value.items():
                    formatted_sub_key = sub_key.replace('_', '').capitalize()
                    output.append(f"  {formatted_sub_key}: {sub_value}")
            else:
                # Handle simple values
                output.append(f"  {value}")
            
            # Add spacing between sections
            output.append("")
        
        # Remove the last empty line
        if output and output[-1] == "":
            output.pop()
        
        return '\n'.join(output)
        
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {e}"
    except Exception as e:
        return f"Error formatting data: {e}"
