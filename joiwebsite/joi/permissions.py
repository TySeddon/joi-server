from rest_framework import permissions
import joi.models as models

def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

class IsCarePartnerOfResident(permissions.BasePermission):
    """
    Custom permission to only allow CarePartners of Resident to view and edit Resident's data
    Admins have access.
    This permission should only be applied to objects that have a "resident" field.
    """
    def has_object_permission(self, request, view, obj):
        if permissions.IsAdminUser().has_permission(request,view):
            return True
        elif is_member(request.user,'Researcher'):
            return True       
        else:
            # see if user is resident
            resident = models.Resident.objects.filter(user=request.user).first()
            if resident is not None:
                return models.CarePartnerResident.objects.filter(resident_id=resident.resident_id).exists()
            else:
                # see if user is care partner
                user_carepartner = models.CarePartner.objects.filter(user=request.user).first()
                if user_carepartner is not None:
                    # see if this CarePartner is associated with Resident of this object
                    return models.CarePartnerResident.objects.filter(resident_id=obj.resident_id, carepartner=user_carepartner).exists()
                else:
                    return False

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
        if request.path.startswith('/joi/v1/users/'):
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

