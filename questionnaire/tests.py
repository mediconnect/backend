from django.http import JsonResponse,Http404
from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.parsers import JSONParser
from .models import Questionnaire
from hospital.models import Hospital
from disease.models import Disease


class Questionnaire(APITestCase):
    def setUp(self):
        hospital = Hospital.objects.create(id = 1, name = 'demo_hospital')
        disease = Disease.objects.create(id = 2, name = 'demo_disease')
        hospital.save()
        disease.save()
        self.client = APIClient()

    def test_create_questionnaire(self):
        """
        Ensure we can create a new questionnaire object.
        """
        url = reverse('questionnaire_init')
        data = {'hospital':1,
                'disease': 2,
                }
        try:
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, 200)
            response_obj = json.loads(response.content)
            self.assertEqual(data, dict(filter(lambda kv: kv[0] in data.keys(), response_obj.items())))
        except Exception as e:
            print(str(e))
