from django.db import models
from customer.models import Customer
from patient.models import Patient


class Reservation(models.Model):
    class Meta:
        db_table = 'db_reservation'
        
