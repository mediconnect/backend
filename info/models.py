from django.db import models
from hospital.models import Hospital
from disease.models import Disease
import uuid
# Create your models here.


class Info(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True,
                                 related_name='hospital_price')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True,
                                related_name='disease_price')
    rank = models.IntegerField(default=0)
    deposit = models.IntegerField(default=10000)
    full_price = models.IntegerField(default=100000)
    description = models.TextField(default='information')

    class Meta:
        db_table = 'db_info'
