from django.shortcuts import redirect, get_list_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from .utils import build_thread

# Create your views here.

User = get_user_model()
@login_required
def delete_user(request):
    '''Allow a logged-in user to delete their account'''
    user = request.user
    logout(request) # log out before deleting
    user.delete()  # trigger post_delete signals
    return redirect('home') # Redirect to homepage after deletion



def get_conversation(request, user_id):
    '''Fetch conversation between current user and the other user with the replies included'''
    messages = (
        Message.objects.filter(receiver_id=user_id)
        .select_related('sender', 'receiver', 'parent_message') # optimize FKS
        .prefetch_related('replies')
        .order_by('created_at')
    )

    data = [
        {
            'id':msg.id,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'replies': [
                {
                    'id':r.id, 'content': r.content, 'sender': r.sender.username
                }
                for r in msg.replies.all()
            ],
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)

def get_message_thread(request, message_id):
    '''Get the thread message from both the sender and replies'''
    root_message = get_list_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'), id=message_id
    )

    thread = build_thread(root_message)
    return JsonResponse(thread, safe=False)


