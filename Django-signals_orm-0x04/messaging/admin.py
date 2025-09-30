from django.contrib import admin
from .models import Message, Notification

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Create a class model admin'''
    list_display = ('id', 'sender', 'receiver', 'timestamp')

@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    '''Class notifications model admin'''
    list_display = ('id', 'message', 'created_at', 'is_read')
