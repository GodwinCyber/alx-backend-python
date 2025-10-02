from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory
from django.db.models import Q

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
        
    def test_user_deletion_cleans_related_data(self):
        '''Deleting user should delete their messages, notification, and histories'''
        self.message.content = 'Edited once'
        self.message.save() # create history

        self.sender.delete() # trigger to post_delete

        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(MessageHistory.objects.count(), 0)

# -------------------------------
# Tests for threaded messages
# -------------------------------

class ThreadMessageTestCase(TestCase):
    """
    Test cases for threaded messages between two users.
    Covers:
    - Message threading (direct replies and nested replies)
    - Recursive retrieval of replies
    - Conversation retrieval between two users
    - Query optimization using select_related and prefetch_related
    """

    def setUp(self):
        """Set up test users and threaded messages"""
        self.user1 = User.objects.create_user(username='alice', password='pass123')
        self.user2 = User.objects.create_user(username='bob', password='pass123')

        # Root message
        self.root_msg = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello Bob'
        )

        # Direct reply from Alice
        self.reply1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hi Bob',
            parent_message=self.root_msg
        )

        # Direct reply from Bob
        self.reply_from_bob = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Hi Alice',
            parent_message=self.root_msg
        )

        # Nested reply from Alice
        self.reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='How are you?',
            parent_message=self.reply1
        )

    def test_message_can_have_replies(self):
        """A message should be able to have direct replies"""
        replies = self.root_msg.replies.all()
        self.assertIn(self.reply1, replies)
        self.assertIn(self.reply_from_bob, replies)
        self.assertEqual(replies.count(), 2)

    def test_recursive_replies(self):
        """Messages should be retrievable recursively (nested threading)"""
        reply1_replies = self.reply1.replies.all()
        self.assertIn(self.reply2, reply1_replies)

        # Root message should indirectly lead to reply2 via reply1
        all_replies = self._get_all_replies(self.root_msg)
        self.assertIn(self.reply2, all_replies)

    def _get_all_replies(self, message):
        """Helper method to fetch all replies recursively"""
        replies = list(message.replies.all())
        for reply in message.replies.all():
            replies.extend(self._get_all_replies(reply))
        return replies

    def test_conversation_between_two_user(self):
        """All messages between two users should be retrievable"""
        messages = Message.objects.filter(
            Q(sender=self.user1, receiver=self.user2) |
            Q(sender=self.user2, receiver=self.user1)
        )

        self.assertEqual(messages.count(), 4)
        self.assertIn(self.root_msg, messages)
        self.assertIn(self.reply1, messages)
        self.assertIn(self.reply2, messages)
        self.assertIn(self.reply_from_bob, messages)

    def test_query_optimization(self):
        """Conversation queries should be optimized with select_related and prefetch_related"""
        with self.assertNumQueries(2):
            messages = (
                Message.objects.select_related('sender', 'receiver', 'parent_message')
                .prefetch_related('replies')
                .filter(sender=self.user1, receiver=self.user2)
            )
            for msg in messages:
                list(msg.replies.all())
