from django.db import models
from hospital.models import Hospital
from disease.models import Disease

class FileType(models.Model):

    name = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    obsolete = models.BooleanField(default=False)

    # reserved, unused fields
    extensions = models.TextField(max_length=100, blank=True, null=True)
    limit = models.IntegerField(default=16384)

    class Meta:
        db_table = 'db_requirement_file_type'

class Requirement(models.Model):

    hospital_id = models.ForeignKey(Hospital,null = True, on_delete= models.SET_NULL)
    disease_id = models.ForeignKey(Disease,null = True, on_delete= models.SET_NULL)
    require_list = models.BinaryField()

    class Meta:
        db_table = 'db_requirement'
