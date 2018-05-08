import uuid
from django.db import models
from reservation.models import Reservation

# Create your models here.
class TimeSlot(models.Model):

    timeslot_id = models.UUIDField(primary_key=True, editable=False)
    # foreign key
    hospital_id = models.UUIDField()
    disease_id = models.IntegerField()

    # time
    slot_year = models.IntegerField()
    slot_weeknum = models.IntegerField()
    availability = models.IntegerField()

    # need uuid 5 to ensure reproducibility, hospital id namespace to prevent clash
    @staticmethod
    def createID(hospital_id, disease_id, slot_year, slot_weeknum):
        return uuid.uuid5(
            namespace=hospital_id,
            name="{d}/{yr}{wk}".format(
                d=disease_id, yr=slot_year, wk=slot_weeknum
            )
        )


class SlotBind(models.Model):

    slot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timeslot_id = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)