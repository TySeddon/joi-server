from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user                
        
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to view and edit it
    """

    def has_object_permission(self, request, view, obj):
        if request.path.startswith('/net/v1/users/'):
            return obj.id == request.user.id or permissions.IsAdminUser().has_permission(request,view)
        else:
            return obj.user == request.user or permissions.IsAdminUser().has_permission(request,view)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit, but anyone to view
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return permissions.IsAdminUser().has_permission(request,view)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return permissions.IsAdminUser().has_permission(request,view)

