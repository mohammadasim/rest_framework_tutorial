from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    Currently any authenticated user can edit a snippet created
    by another user.
    """
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we will always allow GET, HEAD, or OPTIONS request.
        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permission are only allow to the owner of the
        # snippet. Return True if the object owner is equal to
        # the request.user
        return obj.owner == request.user
