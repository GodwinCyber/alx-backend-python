from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notifications(sender, instance, created, **kwargs):
    '''Trigger a notification when a new message instance is created'''
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


