from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request):
        '''Allow access only to authenticated users'''
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, obj):
        '''Only the perticipants of the conversation can send, view, update or delete messages'''
        if request.method in SAFE_METHODS:
            # If the object is a Conversation, check if the user is a participant
            return request.user in obj.participants.all()
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Only participants can modify messages or conversations
            return request.user in obj.participants.all()
        return False

