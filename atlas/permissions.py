# rest framework
from rest_framework.permissions import BasePermission

# django

# other
from supervisor.models import Supervisor
from translator.models import Translator
from reservation.models import Reservation

class SupervisorPermission(BasePermission):
    """
        Permission to allow supervisor level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Supervisor.objects.filter(user=user).exists()  # check if user is a supervisor

class TranslatorPermission(BasePermission):
    """
            Permission to allow translator level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Translator.objects.filter(user=user).exists()  # check if user is a supervisor

