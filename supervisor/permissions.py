# rest framework
from rest_framework.permissions import BasePermission

# django

# other
from .models import Supervisor


class SupervisorPermission(BasePermission):
    """
        Permission to allow supervisor level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Supervisor.objects.filter(user=user).exists()  # check if user is a supervisor
