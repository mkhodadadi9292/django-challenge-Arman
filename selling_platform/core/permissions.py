from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the owner of the wallet or an admin
        return obj.user == request.user or request.user.is_staff
