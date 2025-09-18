from rest_framework  import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    ''''
    Serializer for User model.
    Excludes sensitive fields like password.
    '''

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        '''Hash password properly on user creation'''
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

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

    def validate_message_body(self, value):
        '''Ensure message body is not empty'''
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

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

    def get_message_count(self, obj):
        '''Return the number of messages in the conversation'''
        return obj.messages.count()


