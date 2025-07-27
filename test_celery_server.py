
import subprocess
import time
from dashboard.tasks import debug_add, send_admin_message

def check_redis():
    """Check if Redis server is running by sending a PING command."""
    try:
        result = subprocess.run([
            "redis-cli", "PING"
        ], capture_output=True, text=True)
        if result.stdout.strip() == "PONG":
            print("✅ Redis broker is running: PONG")
            return True
        else:
            print(f"❌ Redis broker not running or did not return PONG: {result.stdout.strip()}")
            return False
    except Exception as e:
        print(f"❌ Error checking Redis: {e}")
        return False

def check_celery_debug():
    """Check if Celery is running by calling its debug task."""
    try:
        result = debug_add.delay(3, 5)
        for _ in range(5):
            if result.ready():
                print(f"✅ Celery worker is working: task executed successfully: {result.get()}")
                return True
            time.sleep(1)
        print("❌ Celery worker is not working: task did not complete.")
    except Exception as e:
        print(f"❌ Error checking Celery worker: {e}")
        return False

if __name__ == "__main__":
    check_redis()
    check_celery_debug()
