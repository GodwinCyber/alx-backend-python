from django.db import models
import uuid
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Message(models.Model):
    '''Create Message model class that store message between two user'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sent_message', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receive_message', on_delete=models.CASCADE)
    content = models.TextField()
    edited = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        '''Return the message'''
        return f'From {self.sender} to {self.receiver}: {self.content[:20]}'
    
class Notification(models.Model):
    '''Class Notifications store the message when a user recieve message'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        '''Return stoored message'''
        return f'Notification for {self.user.email} - Message {self.message.id}'


class MessageHistory(models.Model):
    '''Log the old content of a message into a separate model'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_message = models.TextField()
    edited_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return the hostory the message'''
        return f'History for {self.message.id} at {self.edited_by}'


