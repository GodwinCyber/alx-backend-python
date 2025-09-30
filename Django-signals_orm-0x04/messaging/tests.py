from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

# Create your tests here.
class MessageingSignalsTestCase(TestCase):
    '''class Test cases for the sender and receiver'''
    def setUp(self):
        '''Test cases for sender and receiver'''
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
        '''Ensure that a message is created, a notification is automatically generated'''
        
        # Create a message
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, testing the messaging'
        )

        # fetch all notifications for receiver
        notifications = Notification.objects.filter(user=self.receiver)

        self.assertEqual(notifications.count(), 1, 'Notification should be created per message')
        self.assertEqual(notifications.first().message, msg, 'Notification should be linked to the correct message')

    def test_no_duplication(self):
        '''Ensure that message is create once'''

        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Message is sent once'
        )

        # fetching message each time it create
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1, 'Notification is sent each a message is created')


    def test_notification_unread_by_default(self):
        '''Ensure mesasage is unread by default'''

        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Check unread status'
        )
        notify = Notification.objects.filter(user=self.receiver).first()
        self.assertFalse(notify.is_read, 'Notification should be unread when it first created')



