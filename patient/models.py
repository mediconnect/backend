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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True)
    # user_id = models.CharField(max_length=100)

    # mandatory fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name_pinyin = models.CharField(max_length=50)
    last_name_pinyin = models.CharField(max_length=50)
    gender = models.IntegerField(choices=(
        (0, 'M'),
        (1, 'F'),
        (2, 'O')
    ),default=0)
    # gender = models.IntegerField()
    birthdate = models.DateField()
    # relationship = models.IntegerField(choices=(
    #     (0, 'SELF'),
    #     (1, 'RELATIVE'),
    #     (2, 'OTHER')
    # ),default=0)
    relationship = models.IntegerField()
    passport = models.CharField(max_length=20)

    # optional fields
    notes = models.CharField(blank=True, max_length=10000)

    class Meta:
        db_table = 'db_patient'
