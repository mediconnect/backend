# rest framework
from rest_framework.permissions import BasePermission, SAFE_METHODS

# django

# other
from staff.models.supervisor import Supervisor
from staff.models.translator import Translator
from reservation.models import Reservation
from hospital.models import Hospital
from django.contrib.auth.models import User
from customer.models import Customer
from atlas.logger import logger,exception


@exception(logger)
class SupPermission(BasePermission):
    """
        Permission to allow supervisor level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Supervisor.objects.filter(user=user).exists()  # check if user is a supervisor


@exception(logger)
class TransPermission(BasePermission):
    """
            Permission to allow translator level operation.
    """

    def has_permission(self, request, view):
        user = request.user
        return Translator.objects.filter(user=user).exists()  # check if user is a supervisor


@exception(logger)
class ResPermission(BasePermission):
    """
        Permission to allow user related to this res operation
    """

    def has_permission(self, request, view):
        user = request.user
        res = Reservation(id = request.resid)

        return user.id in [res.user_id,res.translator_c2e_id,res.translator_e2c_id]


@exception(logger)
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


@exception(logger)
class StatusPermission(BasePermission):
    """
    Permission to allow certain operation on object if is at certain stage of reservation,
    should always be used with another user-type permission
    """
    def __init__(self, allowed_status = [], allowed_trans_status = []):

        super(StatusPermission,self).__init__()
        self.allowed_status = allowed_status
        self.allowed_trans_status = allowed_trans_status

    def has_object_permission(self,request,view,obj):
        allowed_status = []
        allowed_trans_status = []
        if obj.status < 1:
            return StatusPermission()  # no status change allowed
        elif obj.status < 7:
            allowed_status = [obj.status - 1, obj.status + 1]
            if obj.trans_status < 5:
                if obj.trans_status < 1:
                    return StatusPermission(allowed_status=allowed_status)
                else:
                    allowed_trans_status = [obj.trans_status - 1, obj.trans_status + 1]
                    return StatusPermission(allowed_status=allowed_status,
                                            allowed_trans_status=allowed_trans_status)
            else:
                if obj.trans_status < 12:
                    if obj.trans_status < 6:
                        return StatusPermission(allowed_status=allowed_status)
                    else:
                        allowed_trans_status = [obj.trans_status - 1, obj.trans_status + 1]
                        return StatusPermission(allowed_status=allowed_status,
                                                allowed_trans_status=allowed_trans_status)
        status = obj.status
        trans_status = obj.trans_status

        if status in self.allowed_status and trans_status in self.allowed_trans_status:
            return True


@exception(logger)
class CanReviewPermission(BasePermission):
    """
    Permission to allow customer add reviews to hospital
    """
    def has_permission(self,request,view):
        hospital = Hospital.objects.get(id = request.data['hospital_id'])
        customer = Customer.objects.get(user = request.user)