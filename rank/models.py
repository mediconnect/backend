from django.db import models

from hospital.models import Hospital
from disease.models import Disease
# Create your models here.


class Rank(models.Model):
    rank = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital, unique=False, default=None, on_delete=models.SET_NULL, null=True,
                                 related_name='hospital_rank')
    disease = models.ForeignKey(Disease, unique=False, default=None, on_delete=models.SET_NULL, null=True,
                                related_name='disease_rank')

    class Meta:
        db_table = 'db_rank'