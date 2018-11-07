from django.db import models
from django.utils import http

from customer.models import Customer
from disease.models import Disease

import uuid


def hospital_directory_path(instance, filename):
    return 'res_{0}/{1}'.format(instance.resid.res_id,http.urlquote(filename))


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
    feedback_time = models.IntegerField(default=1)
    average_score = models.DecimalField(max_digits=4,decimal_places=3,null=True)
    review_number = models.IntegerField(default = 0, null = False)

    class Meta:
        db_table = 'db_hospital'

    def update_score(self, score):
        if self.review_number == 0:
            assert self.average_score is None, 'average score is not consistent with review number, something went wrong.'
            self.average_score = score
            self.review_number = 1
        else:
            self.average_score = (self.average_score * self.review_number + score) / (self.review_number + 1)
            self.review_number += 1


class HospitalReview(models.Model):

    hospital = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    review = models.CharField(null = True,max_length=200)
    score = models.IntegerField(null = True)

    class Meta:
        db_table = 'db_hospital_review'


class LikeHospital(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, unique=False, default=None, null=True,)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, unique=False, default=None, null=True,)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, unique=False, default=None, null=True,)

    class Meta:
        db_table = 'db_like_hospital'