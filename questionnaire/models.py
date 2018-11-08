import os
import uuid

from django.db import models
from staff.models.translator import Translator
from hospital.models import Hospital
from disease.models import Disease
from reservation.models import Reservation


def questions_path(instance, filename):
    return 'hospital_{0}/disease_{1}/{2}_question{3}'\
        .format(instance.hospital.name,
                instance.disease.name,
                os.path.split(filename)[0],
                os.path.split(filename)[1])


def origin_questions_path(instance, filename):
    return 'hospital_{0}/disease_{1}/{2}_origin{3}'\
        .format(instance.hospital.name,
                instance.disease.name,
                os.path.split(filename)[0],
                os.path.split(filename)[1])


def translated_questions_path(instance, filename):
    return 'hospital_{0}/disease_{1}/{2}_translated{3}'\
        .format(instance.hospital.name,
                instance.disease.name,
                os.path.split(filename)[0],
                os.path.split(filename)[1])


FORMAT_CHOICES = (
    (1, 'Multiple Choice'),
    (2, 'All that Matched'),
    (3, 'Short Answer'),
)


class Questionnaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital,on_delete= models.SET_NULL, null=True)
    disease = models.ForeignKey(Disease, on_delete= models.SET_NULL, null=True)
    category = models.CharField(max_length=200, blank=True)
    # questions = models.FileField(upload_to=questions_path, null=True)
    is_translated = models.BooleanField(default=False)
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True)
    origin = models.FileField(upload_to=origin_questions_path, null=True)
    translated = models.FileField(upload_to=translated_questions_path, null=True)

    class Meta:
        db_table = 'db_questionnaire'


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionnaire = models.ForeignKey(Questionnaire,on_delete=models.SET_NULL, null=True)
    format = models.IntegerField(choices=FORMAT_CHOICES)
    content = models.CharField(max_length=200)

    class Meta:
        db_table = 'db_question'


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question,on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)

    class Meta:
        db_table = 'db_choice'


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)
    questionnaire= models.ForeignKey(Questionnaire, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=500, blank=True)
    is_translated = models.BooleanField(default=False)
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True)
    origin = models.FileField(upload_to=origin_questions_path, null=True)
    translated = models.FileField(upload_to=translated_questions_path, null=True)

    class Meta:
        db_table = 'db_answer'
