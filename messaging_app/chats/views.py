from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    '''ViewSet for listing and creating conversations'''
    serializer_class = ConversationSerializer # Use ConversationSerializer for serialization
    http_method_names = ['get', 'post'] # Allow only GET and POST methods
    filterset_fields = ['participants'] # Allow filtering by participants
    search_fields = ['title'] # Allow searching by title
    ordering_fields = ['created_at'] # Allow ordering by creation date
    ordering = ['-created_at'] # Default ordering by creation date descending
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] # Custom permission to check if user is a participant

    def get_queryset(self):
        '''Return conversations where the user is a participant'''
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    '''ViewSet for listing and creating messages'''
    serializer_class = MessageSerializer # Use MessageSerializer for serialization
    http_method_names = ['get', 'post'] # Allow only GET and POST methods
    filterset_fields = ['conversation', 'sender'] # Allow filtering by conversation and sender
    search_fields = ['content'] # Allow searching by content
    ordering_fields = ['created_at'] # Allow ordering by creation date
    ordering = ['-created_at'] # Default ordering by creation date descending
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] # Custom permission to check if user is a participant

    def get_queryset(self):
        '''Return messages in conversations where the user is a participant'''
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        '''Set the sender to the logged-in user when creating a message'''
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if self.request.user not in conversation.participants.all():
            return Response({'error': 'You are not a participant of this conversation.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user, conversation=conversation)


