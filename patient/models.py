from django.db import models
from customer.models import Customer

class Patient(models.Model):
    """
        Patient model = Patient information storage

        Arguments:
            user_id	Number
            first_name	String
            last_name	String
            first_name_pinyin	String
            last_name_pinyin	String
            gender	String
            birthdate	DateTime
            relationship	String
            passport_number	String

            note <optional>	String
    """
    user_id = models.OneToOneField(Customer, on_delete=models.CASCADE)

    # mandatory fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name_pinyin = models.CharField(max_length=50)
    last_name_pinyin = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ))
    birthdate = models.DateField()
    relationship = models.CharField(max_length=50)
    passport = models.CharField(max_length=20)

    # optional fields
    notes = models.CharField(blank=True, max_length=10000)

    class Meta:
        db_table = 'db_patient'

    def get_name(self):
        """
            Get customer name.

            Return:
                Customer full name if it exists, otherwise username.
        """
        name = self.first_name + ' ' + self.last_name
        return name
