
import os

from django.db import models
import django.utils.encoding as encode
from django.utils import http
from django.conf import settings

from translator.models import Translator
from supervisor.models import Supervisor
from hospital.models import Hospital
from disease.models import Disease

def questions_path(instance, filename):
    return 'hospital_{0}/disease_{1}/{2}'.format(instance.hospital.get_id(), instance.disease.get_id(), http.urlquote(filename))
# Create your models here.
class Questionnaire(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete= models.SET_NULL, null = True)
    disease = models.ForeignKey(Disease, on_delete= models.SET_NULL, null = True)
    category = models.CharField(max_length=200, blank=True)
    questions = models.FileField(upload_to=questions_path, null=True)
    questions_path = models.CharField(max_length = 200)
    is_translated = models.BooleanField(default=False)
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True)
    origin_pdf = models.FileField(upload_to=questions_path,null=True)
    origin_pdf_path = models.CharField(max_length= 200)

    class Meta:
        db_table = 'questionnaire'

    def save(self, *args, **kwargs):  # override_save method
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.questions_path = questions_path(self, self.questions)
        self.origin_pdf_path = questions_path(self,self.origin_pdf)
        super(Questionnaire, self).save(*args, **kwargs)

    def get_questions_name(self):
        return self.category+' 问题模板: '+ encode.uri_to_iri(self.questions_path)

    def get_origin_pdf_name(self):
        return self.category+' 原始pdf: '+ encode.uri_to_iri(self.origin_pdf_path)

    def get_questions_path(self):
        return (self.questions_path[(str.find(str(self.questions_path), '%')):], str(os.path.join(settings.MEDIA_ROOT, str(self.questions))))

    def get_origin_pdf_path(self):
        return (self.origin_pdf_path[(str.find(str(self.origin_pdf_path), '%')):], str(os.path.join(settings.MEDIA_ROOT, str(self.origin_pdf))))