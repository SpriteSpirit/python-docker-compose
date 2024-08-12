from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Moderators').exists())
