from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.TextChoices):
    ''' User roles within the messaging application.'''
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'

class User(AbstractUser):
    '''
    Custom User model extending AbstractUser to match project specification.
    Uses UUID as primary key and includes additional fields (phone_number, role)
    '''
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name='email address')
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, null=False, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)

    # custom user model settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        '''String respresntation of User model'''
        return f'{self.first_name} {self.last_name} ({self.email})'

class Conversation(models.Model):
    '''
    Conversation model to track users involved in a conversation.
    Many-to-Many relationship with User.
    '''
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''String respresentation of Conversation model'''
        return f'Conversation {self.conversation_id}'

class Message(models.Model):
    '''Message model containing sender, conversation, message body, and timestamp.'''
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

