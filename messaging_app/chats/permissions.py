from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        '''Only the perticipants of the conversation can send, view, update or delete messages'''
        if hasattr(obj, 'perticipants'):
            # If the object is a Conversation, check if the user is a participant
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # If the object is a Message, check if the user is a participant in the related conversation
            return request.user in obj.conversation.participants.all()
        return False
