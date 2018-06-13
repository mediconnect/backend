import uuid
from django.db import models
from customer.models import Customer
from patient.models import Patient
from translator.models import Translator
from slot.models.timeslot import TimeSlot


class Reservation(models.Model):

    # id - auto generated uuid
    res_id = models.UUIDField(primary_key=True, editable=False)
    # foreign key fields
    user_id = models.UUIDField()
    patient_id = models.IntegerField()
    translator_c2e_id = models.ForeignKey(Translator)
    translator_e2c_id = models.ForeignKey(Translator)
    hospital_id = models.UUIDField()
    disease_id = models.IntegerField()
    commit_at = models.DateTimeField(null=True, blank=True)

    # payment - use one to many join to discover

    # reservation create time
    ctime = models.DateTimeField(auto_now_add=True)

    # reservation time slot id
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
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
