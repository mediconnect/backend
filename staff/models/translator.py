# django
from django.db import models
from django.contrib.auth.models import User
import uuid
# rest framework

# other

C2E = 0
E2C = 1


class Translator(models.Model):
    """
        Translator model for handling translator assisting the reservation.

        Arguments:
            user: one-to-one field appended to default User table.
            role: translator type
    """

    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(default=C2E)

    class Meta:
        db_table = 'db_translator'