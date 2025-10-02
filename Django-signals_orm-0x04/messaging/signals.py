from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notifications(sender, instance, created, **kwargs):
    '''Trigger a notification when a new message instance is created'''
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )

@receiver(pre_save, sender=Message)
def log_message_edited(sender, instance, **kwargs):
    if not instance.pk:
        # Skip new messages
        return
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_message=old_message.content,
            edited_by=instance.sender
        )
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_delete(sender, instance, **kwargs):
    '''Delete related message, notifications, and histories when a user is deleted'''
    # Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notification belong to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where user edited
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Delete message histories tied to the message of this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete() # Where message__sender is the message instances that related to the sender, lookup

