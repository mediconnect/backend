from django.db import models
from django.contrib.auth.models import User
import uuid


class Supervisor(models.Model):
    """
        Supervisor model for handling supervisor administrating the website.

        Arguments:
            user: one-to-one field appended to default User table.
    """
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_supervisor'
