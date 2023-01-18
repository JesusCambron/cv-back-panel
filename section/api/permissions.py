from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):

  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      # Check permissions for read-only request
      return True
    else:
      # Check permissions for write request
      return bool(request.user and request.user.is_staff)