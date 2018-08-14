from django.db import models
from django.contrib.auth.models import User


class Supervisor(models.Model):
    """
        Supervisor model for handling supervisor administrating the website.

        Arguments:
            user: one-to-one field appended to default User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_supervisor'
