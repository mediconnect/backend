from django.db import models
from hospital.models import Hospital
from disease.models import Disease
from customer.models import Customer
import uuid
# Create your models here.


class Info(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True,
                                 related_name='hospital_price')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True,
                                related_name='disease_price')
    rank = models.IntegerField(default=0)
    deposit = models.IntegerField(default=10000)
    full_price = models.IntegerField(default=100000)
    description = models.TextField(default='information')
    feedback_time = models.IntegerField(default=1)
    average_score = models.FloatField(default=0.0)
    review_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'db_info'


class InfoReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    info = models.ForeignKey(Info,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    review = models.CharField(null=True,max_length=500)
    score = models.IntegerField(null=True)
    review_time = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        db_table = 'db_info_review'


class LikeInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, unique=False, default=None, null=True,)
    info = models.ForeignKey(Info, on_delete=models.SET_NULL, unique=False, default=None, null=True)
    like_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'db_like_info'
