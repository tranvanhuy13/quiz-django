from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """
    Allows access only to users with the Teacher role.
    """

    def has_permission(self, request, view):
        return (
            hasattr(request.user, "userprofile")
            and request.user.userprofile.role == "Teacher"
        )


class IsStudent(BasePermission):
    """
    Allows access only to users with the Student role.
    """

    def has_permission(self, request, view):
        return (
            hasattr(request.user, "userprofile")
            and request.user.userprofile.role == "Student"
        )

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects, others can only read.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        # Write permissions are only allowed to the owner or admin
        return obj.user == request.user or request.user.is_staff
