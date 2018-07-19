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
    return 'order_{0}/{1}/{2}'.format(instance.res.customer.get_name().strip(' '), instance.res.id,
                                      http.urlquote(filename))


class Document(models.Model):
    id = models.UUIDField(primary_key= True, default = uuid.uuid4,editable = False)
    resid = models.ForeignKey(Reservation,on_delete = models.SET_NULL, null=True)
    owner = models.ForeignKey(User,on_delete = models.SET_NULL, null = True)
    description = models.CharField(max_length=50, blank=True)
    upload_at = models.DateTimeField(auto_now_add = True)
    data = models.FileField(upload_to=res_directory_path)
    obsolete = models.BooleanField(default=False)
    type = models.IntegerField(default = ORIGINAL)

    # reserved, unused fields
    extensions = models.TextField(max_length=100, blank=True, null=True)
    limit = models.IntegerField(default=16384)

    class Meta:
        db_table = 'db_document'