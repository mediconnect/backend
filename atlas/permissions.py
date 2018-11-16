# rest framework
from rest_framework.permissions import BasePermission, SAFE_METHODS

# django

# other
from staff.models.supervisor import Supervisor
from staff.models.translator import Translator
from reservation.models import Reservation
from info.models import Info, InfoReview
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

    def has_object_permission(self, request, view, obj):
        user = request.user
        res = obj
        try:
            if Customer.objects.filter(user=user).exists():
                assert res.user_id == user.id
                return True
            elif Translator.objects.filter(user=user).exists():
                trans = Translator.objects.get(user=user)
                if trans.role == 0:  # C2E
                    assert res.trans_status < 5 # TODO: specify status
                    return True
                elif trans.role == 1:  # E2C
                    assert res.trans_status > 5
                    assert  res.trans_status < 10
                    return True
            else:
                return False
        except AssertionError:
            return False


@exception(logger)
class IsOwner(BasePermission):
    """
    Owner here is abstract,
     e.g. customer/4/patient/1, patient 1's 'owner' is customer 4
          questionnaire/1/question/2/choice/3, choice 3 's owner is question 2 whose owner is questionnaire 4

    """
    def has_permission(self, request, view):
        if 'customer_id' in view.kwargs:
            return Customer.objects.get(id=view.kwargs['customer_id']).user == request.user

    def has_object_permission(self, request, view, obj):
        for k,v in view.kwargs.items():
            if k == 'pk':
                continue
            if '_id' in k and not isinstance(obj,Reservation):
                k = k.replace('_id','')
            if obj.__getattribute__(k).id != int(v):
                return False
        return True


class IsOwnerOrStaff(BasePermission):
    """
    Owner or supervisor permission
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if Supervisor.objects.filter(user=user).exists():
            return True
        elif Translator.objects.filter(user=user).exists():
            if request.method in SAFE_METHODS:
                return True
            else:
                return False
        else:
            return IsOwner().has_object_permission(request,view,obj)


@exception(logger)
class StatusPermission(BasePermission):
    """
    Permission to allow certain operation on object if is at certain stage of reservation,
    should always be used with another user-type permission
    """
    def __init__(self, allowed_status=None, allowed_trans_status=None):
        if not allowed_status:
            allowed_status = []
        if not allowed_trans_status:
            allowed_trans_status = []
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
        if request.method in SAFE_METHODS:
            return True
        info = Info.objects.get(id=request.data['info_id'])
        hospital_id = info.hospital.id
        disease_id= info.disease.id
        customer_id = Customer.objects.get(user=request.user).id
        if Reservation.objects.filter(user_id=customer_id,
                                      hospital=hospital_id,
                                      disease_id=disease_id).exists():
            if InfoReview.objects.filter(customer_id=customer_id,info=info).exists():
                return request.method in ['PUT','DELETE',]

            else:
                return request.method == 'POST'
