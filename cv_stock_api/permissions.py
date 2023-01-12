from rest_framework import permissions


class IsOwnerAndAuthOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return obj.owner.instance.user == request.user
