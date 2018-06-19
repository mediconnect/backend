# rest framework
from rest_framework.permissions import BasePermission, SAFE_METHODS

# django

# other
from supervisor.models import Supervisor
from translator.models import Translator
from reservation.models import Reservation

class SupPermission(BasePermission):
    """
        Permission to allow supervisor level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Supervisor.objects.filter(user=user).exists()  # check if user is a supervisor


class TransPermission(BasePermission):
    """
            Permission to allow translator level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Translator.objects.filter(user=user ).exists()  # check if user is a supervisor


class ResPermission(BasePermission):
    """
        Permission to allow user related to this res operation
    """

    def has_permission(self, request, view):
        user = request.user
        res = Reservation(id = request.resid)

        return user.id in [res.user_id,res.translator_c2e_id,res.translator_e2c_id]


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

class StatusPermission(BasePermission):
    """
    Permission to allow certain operation on object if is at certain stage of reservation,
    should always be used with another user-type permission
    """
    def __init__(self, allowed_status = [], allowed_trans_status = []):
        
        super(StatusPermission,self).__init__()
        self.allowed_status = allowed_status
        self.allowed_trans_status = allowed_trans_status

    def has_permission(self,request,view):

        res = Reservation(id = request.resid)
        status = res.status
        trans_status = res.trans_status

        if status in self.allowed_status and trans_status in self.allowed_trans_status
            return True