from django.db import models
from django.utils import http

import uuid


def hospital_directory_path(instance, filename):
    return 'hospital/{0}/{1}'.format(instance.id,http.urlquote(filename))


class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=hospital_directory_path, null=True)
    email = models.EmailField(blank=True)
    area = models.CharField(blank=True, max_length=50)
    overall_rank = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    introduction = models.TextField(default='intro')
    specialty = models.TextField(default='specialty')

    # Deprecated fields
    average_score = models.FloatField(default=0.0)
    review_number = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = 'db_hospital'
