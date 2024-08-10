from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('list', 'retrieve'):
            return request.user.is_authenticated
    
        return request.user.is_superuser or request.user.is_staff
