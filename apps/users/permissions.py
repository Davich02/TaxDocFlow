from rest_framework import permissions

class IsSteuerberater(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Steuerberater').exists()
