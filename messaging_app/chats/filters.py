import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    '''Message filer to your views to retrieve conversations with specific users or messages within a time range'''
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    sender = django_filters.NumberFilter(field_name='sender__id')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        '''Meta class to specify model and fields'''
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']
