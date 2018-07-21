import uuid
from django.db import models
from customer.models import Customer
from patient.models import Patient
from translator.models import Translator
from hospital.models import Hospital
from disease.models import Disease
from slot.models.timeslot import TimeSlot

# Status Code
STARTED = 0  # 下单中
PAID = 1  # order paid 已付款
TRANSLATING_ORIGIN = 2  # translator starts translating origin documents 翻译原件中
SUBMITTED = 3  # origin documents translated, approved and submitted to hospitals 已提交
# ============ Above is C2E status =============#
# ============Below is E2C status ==============#
RETURN = 4  # hospital returns feedback
TRANSLATING_FEEDBACK = 5  # translator starts translating feedback documents 翻译反馈中
FEEDBACK = 6  # feedback documents translated, approved, and feedback to customer 已反馈
DONE = 7  # customer confirm all process done 完成

# Trans Status Code
C2E_NOT_STARTED = 0  # c2e translation not started yet 未开始
C2E_ONGOING = 1  # c2e translation started not submitted to supervisor 翻译中
C2E_APPROVING = 2  # c2e translation submitted to supervisor for approval 审核中
C2E_APPROVED = 4  # c2e translation approved, to status 5 已审核
C2E_DISAPPROVED = 3  # c2e translation disapproved, return to status 1 未批准
C2E_FINISHED = 5  # c2e translation approved and finished for the first half 完成
E2C_NOT_STARTED = 6
E2C_ONGOING = 7
E2C_APPROVING = 8
E2C_APPROVED = 10
E2C_DISAPPROVED = 9
E2C_FINISHED = 11
ALL_FINISHED = 12


class Reservation(models.Model):

    # id - auto generated uuid
    res_id = models.UUIDField(primary_key=True, editable=False)
    # foreign key fields
    user_id = models.ForeignKey(Customer,on_delete=models.SET_NULL, null = True)
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null = True)
    translator_id = models.ForeignKey(Translator,unique=False,on_delete=models.SET_NULL, null = True)
    hospital_id = models.ForeignKey(Hospital,on_delete = models.SET_NULL, null = True)
    disease_id = models.ForeignKey(Disease,on_delete = models.SET_NULL,null = True)
    commit_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default = STARTED)
    trans_status = models.IntegerField(default = C2E_NOT_STARTED)
    # payment - use one to many join to discover

    # reservation create time
    ctime = models.DateTimeField(auto_now_add=True)

    # reservation time slot id
    # timeslot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    # join slot table to get res_start_date

    # ! The blank=True below here does not mean optional.
    # On the creation of the reservation object, these fields are not fillable

    # first diagnosis info
    first_hospital = models.CharField(max_length=300, blank=True)
    first_doctor_name = models.CharField(max_length=100, blank=True)
    first_doctor_contact = models.CharField(max_length=100, blank=True)

    note = models.CharField(max_length=1000, blank=True)

    # files - use one to many join to discover

    class Meta:
        db_table = 'db_reservation'
