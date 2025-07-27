from django.test import TestCase

from zproject.celery import app as celery_app
from dashboard.tasks import (
    debug_add,
    send_admin_message,
    call_mickeybot_api
)
from dashboard.models import AlexSSN, StatusChoices
from django.contrib.auth import get_user_model

class CeleryTasksTestCase(TestCase):
    def setUp(self):
        # Set the Celery app to run tasks immediately for testing
        celery_app.conf.task_always_eager = True
        celery_app.conf.task_eager_propagates = True
        self.user = get_user_model().objects.create(username="testuser")

    def test_debug_add_task(self):
        result = debug_add.delay(3, 5)
        self.assertEqual(result.get(), 8, "debug_add task should return the sum of 3 and 5")
    
    def test_send_admin_message_task(self):
        # Assuming send_admin_message sends a message to the admin
        # This is a placeholder test; you may need to mock the Telegram API call
        result = send_admin_message.delay("Test message")
        self.assertTrue(result.get(), "send_admin_message task should complete successfully")

    def test_call_mickeybot_api_task(self):
        # Create a test request object
        req = AlexSSN.objects.create(user=self.user, full_name="John Doe", zip="12345")
        model_name = req.__class__.__name__
        call_mickeybot_api.delay(self.user.id, model_name, req.id)
        req.refresh_from_db()
        self.assertIn(req.status, [StatusChoices.SUCCESS, StatusChoices.FAILED], "Status should be updated after API call")

