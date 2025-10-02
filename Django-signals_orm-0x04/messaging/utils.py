def build_thread(message):
    '''Recursively build threaded replies for a message'''
    return {
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'created_at': message.created_at,
        'replies': [
            build_thread(reply) for reply in message.replies.all().order_by('created_at')
        ],
    }
