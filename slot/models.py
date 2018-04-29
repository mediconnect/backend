import uuid
from django.db import models

# Create your models here.
class Slot(models.Model):

    slot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # foreign key
    hospital_id = models.UUIDField()
    disease_id = models.IntegerField()

    # time
    slot_year = models.IntegerField(max_length=4)
    slot_weeknum = models.IntegerField(max_length=2)
    slot_seq = models.IntegerField()

    # reservation_id
    occupied_res = models.UUIDField(blank=True)