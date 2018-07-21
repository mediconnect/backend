import uuid
from django.db import models
from reservation.models import Reservation
from .timeslot import TimeSlot

class SlotBind(models.Model):

    slot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'db_slotbind'
