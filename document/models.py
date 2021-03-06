from django.db import models
from django.utils import timezone, http
from django.contrib.auth.models import User

from reservation.models import Reservation

import uuid

ORIGINAL = 0
C2E_TRANSLATED = 1
FEEDBACK = 2
E2C_TRANSLATED = 3


def res_directory_path(instance, filename):
    return 'res_{0}/{1}'.format(instance.res,http.urlquote(filename))


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable = False)
    res = models.ForeignKey(Reservation,on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    description = models.CharField(max_length=50, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=res_directory_path)
    obsolete = models.BooleanField(default=False)
    type = models.IntegerField(default=ORIGINAL,choices=(
        (0,'ORIGINAL'),
        (1,'C2E_TRANSLATED'),
        (2,'FEEDBACK'),
        (3,'E2C_TRANSLATED')
    ))

    # reserved, unused fields
    extensions = models.TextField(max_length=100, blank=True, null=True)
    limit = models.IntegerField(default=16384)

    class Meta:
        db_table = 'db_document'