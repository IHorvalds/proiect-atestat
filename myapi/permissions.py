from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Custom permission to only allow owners of an object to edit it.

    def has_obj_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # Allow GET, HEAD, OPTIONS request from anyone. Authed or not
            return True
        return obj.owner == request.user
