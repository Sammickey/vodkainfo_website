#!/bin/bash
# chmod +x start_dev.sh
# ./start_dev.sh

# Activate virtual environment
source .venv/bin/activate

# Start Redis server (requires sudo)
sudo service redis-server start

# Set Django settings module
export DJANGO_SETTINGS_MODULE=zproject.settings_dev

# Start Django server in the background
python manage.py runserver &

# Start Celery worker in the background
python manage.py startcelery &

echo "Development environment started!"
