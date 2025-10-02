from django.db import models

class UnreadMessagesManager(models.Manager):
    '''Custome manager to filter unread message for a user'''

    def unread_for_user(self, user):
        '''
            Return unread message for the given user (as receiver)
            Uses `.only()` and `selected_related` for query optimization
        '''
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .select_related('sender', 'receiver')
            .only('id', 'content', 'sender_username', 'receiver_username', 'created_at')
        )



