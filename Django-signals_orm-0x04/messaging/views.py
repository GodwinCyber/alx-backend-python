from rest_framework import viewsets
from django.shortcuts import get_list_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Notification, MessageHistory
from .serializers import (
    MessageSerializer,
    NotificationSerializer,
    MessageHistorySerializer,
)
from .utils import build_thread
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing, creating, and managing messages."""

    serializer_class = MessageSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sender", "receiver", "parent_message"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return messages involving the logged-in user (as sender or receiver)."""
        user = self.request.user
        return (
            Message.objects.select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
            .filter(Q(sender=user) | Q(receiver=user))
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        """Set the sender as the logged-in user automatically."""
        serializer.save(sender=self.request.user)

    def get_message_thread(request, message_id):
        """Get the thread message from both the sender and replies."""
        # Explicit filter query first
        queryset = Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related("sender", "receiver").prefetch_related("replies")

        # Ensure the message exists within the user's conversation
        root_message = get_list_or_404(queryset, id=message_id)

        # Build recursive thread
        thread = [build_thread(m) for m in root_message]
        return JsonResponse(thread, safe=False)
    
    @login_required
    def unread_inbox(request):
        '''Fetch only unread messages for the logged-in user'''
        unread_messages = (
            Message.unread.unread_for_user(request.user)
            .only('id', 'sender__username', 'receiver__username', 'content', 'created_at')
            .select_related('sender', 'receiver')
        )
        
        data = [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'receiver': msg.receiver.username,
                'content': msg.content,
                'created_at': msg.created_at
            }
            for msg in unread_messages
        ]
        return JsonResponse(data, safe=False)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user notifications."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notifications belonging to the logged-in user."""
        return Notification.objects.filter(user=self.request.user).select_related(
            "message", "user"
        )


class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing history of edited messages."""

    serializer_class = MessageHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return history of messages the logged-in user has access to."""
        user = self.request.user
        return MessageHistory.objects.filter(
            Q(message__sender=user) | Q(message__receiver=user)
        ).select_related("message", "edited_by")



