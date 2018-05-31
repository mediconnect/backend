from django.db import models

class FileType(models.Model):

    name = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    obsolete = models.BooleanField(default=False)

    # reserved, unused fields
    extensions = models.TextField(max_length=100, blank=True, null=True)
    limit = models.IntegerField(default=16384)


class Requirement(models.Model):

    hospital_id = models.UUIDField()
    disease_id = models.IntegerField()
    require_list = models.BinaryField()