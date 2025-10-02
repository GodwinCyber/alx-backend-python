from rest_framework import viewsets
from django.shortcuts import get_list_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Notification, MessageHistory, Conversation
from .serializers import (
    MessageSerializer,
    NotificationSerializer,
    MessageHistorySerializer,
)
from .utils import build_thread
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


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


@method_decorator(cache_page(60), name="dispatch")
class ConversationMessageView(viewsets.ModelViewSet):
    """
    View to fetch all the messages in a conversation.
    Cached for 1 minute to reduce database hits.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ["get", "post", "put", "delete"]
    lookup_field = "id"

    def get_queryset(self):
        """Return messages where the user is either sender or receiver."""
        user = self.request.user
        return (
            Message.objects.select_related("sender", "receiver")
            .prefetch_related("replies")
            .filter(sender=user)
            | Message.objects.select_related("sender", "receiver")
            .prefetch_related("replies")
            .filter(receiver=user)
        ).only("id", "sender", "receiver", "content", "created_at")

    def perform_create(self, serializer):
        """Attach the conversation and sender automatically when creating a message."""
        conversation_id = self.request.data.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)


