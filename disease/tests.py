from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase
import uuid

from .models import Disease

class DiseaseModuleTest(APITestCase):

    def test_create_disease(self):
        """
        Ensure that we can create a hospital
        """
        url = reverse('disease-list')
        data = {
            'id': uuid.uuid4(),
            'name': 'demo_disease',
            'keyword':'demo demo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        disease = Disease.objects.get(name='demo_disease')
