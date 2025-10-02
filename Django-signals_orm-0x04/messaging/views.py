from django.shortcuts import redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()
@login_required
def delete_user(request):
    '''Allow a logged-in user to delete their account'''
    user = request.user
    logout(request) # log out before deleting
    user.delete()  # trigger post_delete signals
    return redirect('home') # Redirect to homepage after deletion

