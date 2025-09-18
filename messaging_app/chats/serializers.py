from rest_framework  import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    ''''
    Serializer for User model.
    Excludes sensitive fields like password.
    '''

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    '''
    Serializer for Message model.
    Includes nested sender (User) details.
    '''
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    ''' 
    Serializer for Conversation model.
    Includes nested participants and messages.
    '''
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['conversation_id', 'created_at']


