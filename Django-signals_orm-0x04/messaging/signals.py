from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


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


