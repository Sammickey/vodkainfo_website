#!/bin/bash
# chmod +x stop_dev.sh
# ./stop_dev.sh

# Stop Django runserver
DJANGO_PIDS=$(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')
if [ -n "$DJANGO_PIDS" ]; then
    echo "Stopping Django runserver: $DJANGO_PIDS"
    kill $DJANGO_PIDS
else
    echo "No Django runserver process found."
fi

# Stop Celery worker
CELERY_PIDS=$(ps aux | grep 'manage.py startcelery' | grep -v grep | awk '{print $2}')
if [ -n "$CELERY_PIDS" ]; then
    echo "Stopping Celery worker: $CELERY_PIDS"
    kill $CELERY_PIDS
else
    echo "No Celery worker process found."
fi

# Stop Redis server
sudo service redis-server stop

echo "Development services stopped!"
