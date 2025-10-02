from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory

User = get_user_model()

# -------------------------------
# Tests for message notifications
# -------------------------------
class MessageNotificationSignalsTestCase(TestCase):
    """Test cases for notifications when messages are created"""

    def setUp(self):
        """Create sender and receiver users"""
        self.sender = User.objects.create_user(
            email='sender@example.com',
            username='sender',
            password='TestPass123!'
        )
        self.receiver = User.objects.create_user(
            email='receiver@example.com',
            username='receiver',
            password='TestPass123!'
        )

    def test_message_created_notification(self):
        """Ensure that when a message is created, a notification is generated"""
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, testing the messaging'
        )

        notifications = Notification.objects.filter(user=self.receiver)

        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, msg)

    def test_no_duplication(self):
        """Ensure that notification is created only once per message"""
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Message is sent once'
        )
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

    def test_notification_unread_by_default(self):
        """Ensure notification is unread by default"""
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Check unread status'
        )
        notify = Notification.objects.filter(user=self.receiver).first()
        self.assertFalse(notify.is_read)


# -------------------------------
# Tests for message history
# -------------------------------
class MessageHistorySignalsTestCase(TestCase):
    """Test cases for message editing and history logging"""

    def setUp(self):
        """Create users and an initial message"""
        self.sender = User.objects.create_user(
            email='sender@example.com',
            username='sender',
            password='TestPass123!'
        )
        self.receiver = User.objects.create_user(
            email='receiver@example.com',
            username='receiver',
            password='TestPass123!'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, this is the original message'
        )

    def test_message_edit_creates_history(self):
        """Editing a message should create a MessageHistory entry"""
        self.message.content = 'This is the updated message.'
        self.message.save()

        history_entries = MessageHistory.objects.filter(message=self.message)

        self.assertEqual(history_entries.count(), 1)
        self.assertEqual(history_entries.first().old_message, 'Hello, this is the original message')
        self.assertTrue(self.message.edited)

    def test_multiple_edits_create_multiple_histories_entries(self):
        """Each edit should create a new history entry"""
        self.message.content = 'First edit.'
        self.message.save()

        self.message.content = 'Second edit'
        self.message.save()

        history_entries = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history_entries.count(), 2)

        old_messages = [h.old_message for h in history_entries]
        self.assertIn('Hello, this is the original message', old_messages)
        self.assertIn('First edit.', old_messages)

        for h in history_entries:
            self.assertEqual(h.edited_by, self.sender)

    def test_no_history_on_new_message(self):
        """Creating a new message should not create a history entry"""
        new_message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Brand new message'
        )
        self.assertEqual(new_message.history.count(), 0)

    def test_history_timestamp(self):
        """History entries should store correct edited_at timestamp"""
        self.message.content = 'Edited content with timestamp check'
        self.message.save()

        history = self.message.history.first()
        self.assertIsNotNone(history.edited_at)
        self.assertLessEqual(history.edited_at, timezone.now())
