from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает GET-запросы всем, а POST/PUT/PATCH/DELETE — только администраторам.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'ADMIN'
        )
