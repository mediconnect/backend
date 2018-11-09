from django.db import models
import uuid


# Create your models here.
class Disease(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(default='unknown', max_length=50)
    keyword = models.CharField(default='unknown', max_length=150)
    full_name = models.CharField(default='unknown',max_length=100)
    name_eng = models.CharField(default='unknown',max_length=150)
    types = models.CharField(default='unknwon',max_length=150)
    target_group = models.CharField(default='unknown',max_length=150)
    introduction = models.CharField(default='unknown',max_length=150)
    categories = models.CharField(default='unknown',max_length=150)

    class Meta:
        db_table = 'db_disease'

