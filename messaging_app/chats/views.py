from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    '''ViewSet for listing and creating conversations'''
    queryset = Conversation.objects.all() # Fetch all conversations
    serializer_class = ConversationSerializer # Use ConversationSerializer for serialization
    http_method_names = ['get', 'post'] # Allow only GET and POST methods
    filterset_fields = ['participants'] # Allow filtering by participants
    search_fields = ['title'] # Allow searching by title
    ordering_fields = ['created_at'] # Allow ordering by creation date
    ordering = ['-created_at'] # Default ordering by creation date descending


class MessageViewSet(viewsets.ModelViewSet):
    '''ViewSet for listing and creating messages'''
    queryset = Message.objects.all() # Fetch all messages
    serializer_class = MessageSerializer # Use MessageSerializer for serialization
    http_method_names = ['get', 'post'] # Allow only GET and POST methods
    filterset_fields = ['conversation', 'sender'] # Allow filtering by conversation and sender
    search_fields = ['content'] # Allow searching by content
    ordering_fields = ['created_at'] # Allow ordering by creation date
    ordering = ['-created_at'] # Default ordering by creation date descending

