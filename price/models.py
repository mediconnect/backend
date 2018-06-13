from django.db import models

# Create your models here.
class Price(models.Model):
    hospital = models.ForeignKey('Hospital', unique=False, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name='hospital_price')
    disease = models.ForeignKey('Disease', unique=False, on_delete=models.SET_NULL, null=True, default=None,
                                related_name='disease_price')
    deposit = models.IntegerField(default=10000)
    full_price = models.IntegerField(default=100000)

    class Meta:
        db_table = 'db_price'
