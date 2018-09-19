
import os

from django.db import models
import django.utils.encoding as encode
from django.utils import http
from django.conf import settings

from staff.models.translator import Translator
from hospital.models import Hospital
from disease.models import Disease

def questions_path(instance, filename):
    return 'hospital_{0}/disease_{1}/{2}'.format(instance.hospital.get_id(), instance.disease.get_id(), http.urlquote(filename))

FORMAT_CHOICES = (
    ('Multiple Choice',1),
    ('All that Matched',2),
    ('Short Answer',3),
)
# Create your models here.
class Questionnaire(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete= models.SET_NULL, null = True)
    disease = models.ForeignKey(Disease, on_delete= models.SET_NULL, null = True)
    category = models.CharField(max_length=200, blank=True)
    questions = models.FileField(upload_to=questions_path, null=True)
    is_translated = models.BooleanField(default=False)
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True)
    origin_pdf = models.FileField(upload_to=questions_path,null=True)

    class Meta:
        db_table = 'db_questionnaire'


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire,on_delete = models.SET_NULL, null = True)
    format = models.IntegerField(choices=FORMAT_CHOICES)
    content = models.CharField(max_length=200)
    answer = models.CharField(max_length = 500)

    class Meta:
        db_table = 'db_question'


class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)
    selected = models.BooleanField(default=False)

    class Meta:
        db_table = 'db_choice'

