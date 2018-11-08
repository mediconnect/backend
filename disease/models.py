from django.db import models
import uuid


# Create your models here.
class Disease(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(default='unknown', max_length=50)
    keyword = models.CharField(default='unknown', max_length=150)

    class Meta:
        db_table = 'db_disease'

