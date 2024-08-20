from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    """ Проверка прав доступа к объекту """
    def has_object_permission(self, request, view, instance):
        return instance.owner == request.user or request.user.groups.filter(name='Moderators').exists()


class IsNotModerator(BasePermission):
    """ Дает доступ только для не-модераторов """

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Moderators').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, instance):
        if request.method in permissions.SAFE_METHODS:
            return True
        return instance.id == request.user.id
