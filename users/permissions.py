from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    """ Проверка прав доступа к объекту """
    def has_object_permission(self, request, view, instance):
        return instance.owner == request.user or request.user.groups.filter(name='Moderators').exists()


class IsNotModerator(BasePermission):
    """ Позволяет доступ только для не-модераторов """

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Moderators').exists()
