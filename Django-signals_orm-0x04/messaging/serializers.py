from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (exclude sensitive fields)."""

    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender/receiver."""

    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "created_at", "timestamp", "edited"]

    def get_replies(self, obj):
        """Return nested replies for a message."""
        return MessageSerializer(obj.replies.all(), many=True).data


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""

    message = MessageSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["id", "created_at", "is_read"]


class MessageHistorySerializer(serializers.ModelSerializer):
    """Serializer for MessageHistory model."""

    message = MessageSerializer(read_only=True)
    edited_by = UserSerializer(read_only=True)

    class Meta:
        model = MessageHistory
        fields = "__all__"
        read_only_fields = ["id", "edited_at"]
