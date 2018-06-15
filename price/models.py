from django.db import models
from hospital.models import Hospital
from disease.models import Disease
# Create your models here.
class Price(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True,
                                 related_name='hospital_price')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True,
                                related_name='disease_price')
    deposit = models.IntegerField(default=10000)
    full_price = models.IntegerField(default=100000)

    class Meta:
        db_table = 'db_price'
