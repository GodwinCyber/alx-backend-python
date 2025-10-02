from django.contrib import admin
from .models import Message, Notification, MessageHistory

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Create a class model admin'''
    list_display = ('id', 'sender', 'receiver', 'edited', 'timestamp')
    search_fields = ('sender__email', 'receiver__email', 'content')
    list_filter = ('edited', 'timestamp')

@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    '''Class notifications model admin'''
    list_display = ('id', 'message', 'created_at', 'is_read')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    '''Class model for message History'''
    list_display = ('id', 'message', 'old_message', 'edited_by')
    search_fields = ('old_message',)
    list_filter = ('edited_by',)
