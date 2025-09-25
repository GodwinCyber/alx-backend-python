from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''Custom the permission: Only onwers can see their own messages/conv1ersations'''

    def has_object_view_permission(self, request, view, obj):
        '''Check if the user is the owner of the object'''
        return obj.user == request.user