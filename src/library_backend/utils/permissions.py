from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """ Кастомный класс привелегий пользователя """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_staff and request.user.is_authenticated)
